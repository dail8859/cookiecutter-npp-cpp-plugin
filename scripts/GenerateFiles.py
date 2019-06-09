import Face
from FileGenerator import Regenerate

indent = "\t"

def translateType(t):
	#if t == "void": return "void"
	#if t == "int": return "int"
	#if t == "bool": return "bool"
	if t == "cells": return "const Cell*"
	if t == "colour": return "Colour"
	if t == "position": return "int"
	if t == "textrange": return "Sci_TextRange*"
	if t == "findtext": return "Sci_TextToFind*"
	if t == "formatrange": return "Sci_RangeToFormat*"
	if t == "keymod": return "KeyModifier"
	if t == "string": return "const char*"
	if t == "stringresult": return "char*"
	return t

def translateTypeCpp(t):
	t = translateType(t)
	if t == "const char*": return "const std::string&"
	if t == "char*": return "std::string&"
	return t

def translateFunction(v, name, typeTranslator):
	param1Type = typeTranslator(v["Param1Type"])
	param1Name = v["Param1Name"]
	param2Type = typeTranslator(v["Param2Type"])
	param2Name = v["Param2Name"]
	returnType = typeTranslator(v["ReturnType"])

	# Some functions deal with pointers and "ints" are not appropriate for these
	if name in ["GetDirectFunction", "GetDirectPointer", "GetDocPointer", "CreateDocument"]:
		returnType = "sptr_t"
	elif name in ["GetCharacterPointer", "GetRangePointer"]:
		returnType = "const char*" # keep this even for C++
	elif name in ["PrivateLexerCall", "SetDocPointer", "AddRefDocument", "ReleaseDocument"]:
		param2Type = "sptr_t"

	return returnType, param1Type, param1Name, param2Type, param2Name

def appendComment(indent, out, v):
	if "Comment" in v: 
		if len (v["Comment"]) == 1: 
			out.append(indent + "/// <summary>" + v["Comment"][0] + " (Scintilla feature " + v["Value"] + ")</summary>")
		else:
			out.append(indent + "/// <summary>")
			out.extend([indent + "/// " + line for line in v["Comment"]])
			out.append(indent + "/// (Scintilla feature " + v["Value"] + ")")
			out.append(indent + "/// </summary>")

def appendCallAndReturn(indent, out, returnType, featureConstant, firstArg, seconArg):
	if returnType == "void":
		out.append(indent + "Call(" +featureConstant+ ", " +firstArg+ ", " +seconArg+ ");")
	elif returnType == "std::string":
		out.append(indent + "Call(" +featureConstant+ ", " +firstArg+ ", &" +seconArg+ "[0]);")
		out.append(indent + "trim(" + seconArg + ");")
		out.append(indent + "return " + seconArg + ";")
	elif returnType == "sptr_t":
		out.append(indent + "return Call(" +featureConstant+ ", " +firstArg+ ", " +seconArg+ ");")
	else:
		out.append(indent + "sptr_t res = Call(" +featureConstant+ ", " +firstArg+ ", " +seconArg+ ");")

		if returnType == "bool":
			out.append(indent + "return res != 0;")
		elif returnType == "const char*":
			out.append(indent + "return reinterpret_cast<" +returnType+ ">(res);")
		else:
			out.append(indent + "return static_cast<" +returnType+ ">(res);")
		#else:
		#	out.append(indent + "return res;")

def getParameterList(param1Type, param1Name, param2Type, param2Name):
	first  = param1Type + " " + param1Name if param1Type else ""
	second = param2Type + " " + param2Name if param2Type else ""
	separator = ", " if first and second else ""
	return first + separator + second

def getMethodDefinition(indent, returnType, name, param1Type, param1Name, param2Type, param2Name):
	return indent + returnType + " " + name + "(" + getParameterList(param1Type, param1Name, param2Type, param2Name) +") const {"

def cppMethod(v, out, indent, name):
	if v["Param1Type"] not in ["string", "stringresult"] and  v["Param2Type"] not in ["string", "stringresult"]:
		return

	iindent = indent + "\t"
	returnType, param1Type, param1Name, param2Type, param2Name = translateFunction(v, name, translateTypeCpp)

	firstArg = ""
	seconArg = ""
	firstParamIsStringLen = False

	if v["Param1Type"] == "string":
		firstArg = param1Name + ".c_str()"

	if v["Param2Type"] == "string":
		seconArg = param2Name + ".c_str()"

	if v["Param1Type"] == "int" and v["Param1Name"] == "length":# and v["Param2Type"] == "string":
		param1Type = None
		firstArg = param2Name + ".length()"
		firstParamIsStringLen = True

	if v["Param2Type"] == "stringresult":
		returnType = "std::string"
		param2Type = None

	if len(firstArg) == 0:
		firstArg = param1Name or "SCI_UNUSED"
	if len(seconArg) == 0:
		seconArg = param2Name or "SCI_UNUSED"

	out.append(getMethodDefinition(indent, returnType, name, param1Type, param1Name, param2Type, param2Name))
	featureConstant = "SCI_" + name.upper()

	if v["Param2Type"] == "stringresult":
		out.append(iindent + "auto size = " + "Call(" + featureConstant + ", " + ("SCI_UNUSED" if firstParamIsStringLen else firstArg) + ", NULL);")
		out.append(iindent + "std::string " + param2Name + "(size + 1, '\\0');")

	appendCallAndReturn(iindent, out, returnType, featureConstant, firstArg, seconArg)

	out.append(indent + "}")
	out.append("")


def simpleMethod(v, out, indent, name):
	iindent = indent + "\t"

	returnType, param1Type, param1Name, param2Type, param2Name = translateFunction(v, name, translateType)

	out.append(getMethodDefinition(indent, returnType, name, param1Type, param1Name, param2Type, param2Name))

	featureConstant = "SCI_" + name.upper()

	firstArg = param1Name or "SCI_UNUSED"
	seconArg = param2Name or "SCI_UNUSED"

	appendCallAndReturn(iindent, out, returnType, featureConstant, firstArg, seconArg)

	out.append(indent + "}")
	out.append("")

def printLexGatewayFile(f):
	out = [""]

	for name in f.order:
		v = f.features[name]

		iindent = indent + "\t"

		if v["FeatureType"] in ["fun", "get", "set"] and v["Category"] != "Deprecated":
			simpleMethod(v, out, indent, name)
			cppMethod(v, out, indent, name)

	return out

def main():
	f = Face.Face()
	f.ReadFromFile("Scintilla.iface")
	Regenerate("../{{cookiecutter.plugin_slug}}/src/ScintillaEditor.h", "/* ", printLexGatewayFile(f))

if __name__ == "__main__":
	main()
