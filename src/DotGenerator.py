import hashlib
import sys
if 2 == sys.version_info[0]:
    text = unicode
else:
    text = str

class UmlClass:
    def __init__(self):
        self.fqn = None
        self.parents = []
        self.privateFields = []
        self.privateMethods = []
        self.publicFields = []
        self.publicMethods = []
        self.protectedFields = []
        self.protectedMethods = []

    def addParentByFQN(self, fullyQualifiedClassName):
        self.parents.append(fullyQualifiedClassName)

    def getId(self):
        return "id" + text(hashlib.md5(text(self.fqn).encode('utf-8')).hexdigest())


class DotGenerator:
    _showPrivMembers = False
    _showProtMembers = False
    _showPubMembers = False
    _drawAssociations = False
    _drawInheritances = False

    def __init__(self):
        self.classes = {}

    def hasClass(self, aClass):
        return self.classes.get(aClass) is not None

    def addClass(self, aClass):
        self.classes[aClass.fqn] = aClass

    def _genFields(self, accessPrefix, fields):
        # sort by fieldName
        sorted_fields = sorted(fields, key=lambda x: x[0])
        ret = "".join([(accessPrefix + fieldName + ": " + fieldTypes[0] + "\l") for fieldName, fieldTypes in sorted_fields])
        return ret

    def _genMethods(self, accessPrefix, methods):
        # sort by methodName
        sorted_methods = sorted(methods, key=lambda x: x[1])
        return "".join([(accessPrefix + methodName + methodArgs + " : " + returnType + "\l") for (returnType, methodName, methodArgs) in sorted_methods])

    def _genClass(self, aClass, withPublicMembers=False, withProtectedMembers=False, withPrivateMembers=False):
        c = (aClass.getId()+" [ \n" +
             "   label = \"{" + aClass.fqn)

        if withPublicMembers:
            pubFields = self._genFields('+ ', aClass.publicFields)
            pubMethods = self._genMethods('+ ', aClass.publicMethods)

            if len(pubFields) != 0 or len(pubMethods) != 0:
                c += "|" + pubFields + pubMethods

        if withProtectedMembers:
            protFields = self._genFields('# ', aClass.protectedFields)
            protMethods = self._genMethods('# ', aClass.protectedMethods)

            if len(protFields) != 0 or len(protMethods) != 0:
                c += "|" + protFields + protMethods

        if withPrivateMembers:
            privateFields = self._genFields('- ', aClass.privateFields)
            privateMethods = self._genMethods('- ', aClass.privateMethods)

            if len(privateFields) != 0 or len(privateMethods) != 0:
                c += "|" + privateFields + privateMethods

        c += "}\"  ]\n"
        c = c.replace('<', '\\<')
        c = c.replace('>', '\\>')
        return c

    def _genAssociations(self, aClass):
        edges = set()
        for fieldName, fieldTypes in aClass.privateFields:
            for fieldType in fieldTypes:
                if fieldType in self.classes:
                    c = self.classes[fieldType]
                    edges.add(aClass.getId() + "->" + c.getId())
        for fieldName, fieldTypes in aClass.publicFields:
            for fieldType in fieldTypes:
                if fieldType in self.classes:
                    c = self.classes[fieldType]
                    edges.add(aClass.getId() + "->" + c.getId())
        edgesJoined = "\n".join(edges)
        return edgesJoined+"\n" if edgesJoined != "" else ""

    def _genInheritances(self, aClass):
        edges = ""
        for parent in aClass.parents:
            if parent in self.classes:
                c = self.classes[parent]
                edges += (aClass.getId() + "->" + c.getId() + "\n")
        return edges

    def setDrawInheritances(self, enable):
        self._drawInheritances = enable

    def setDrawAssociations(self, enable):
        self._drawAssociations = enable

    def setShowPrivMethods(self, enable):
        self._showPrivMembers = enable

    def setShowProtMethods(self, enable):
        self._showProtMembers = enable

    def setShowPubMethods(self, enable):
        self._showPubMembers = enable

    def generate(self):
        dotContent = ("digraph dependencies {\n" +
                      "  fontname = \"Bitstream Vera Sans\"\n" +
                      "  fontsize = 8" +
                      "  node [" +
                      "    fontname = \"Bitstream Vera Sans\"\n" +
                      "    fontsize = 8\n" +
                      "    shape = \"record\"\n" +
                      "  ]\n" +
                      "  edge [\n" +
                      "    fontname = \"Bitstream Vera Sans\"\n" +
                      "    fontsize = 8\n" +
                      "  ]\n"
                      )

        for key, value in self.classes.items():
            dotContent += self._genClass(value, self._showPubMembers, self._showProtMembers, self._showPrivMembers)

        # associations
        if self._drawAssociations:
            associations = ""
            for key, aClass in self.classes.items():
                associations += self._genAssociations(aClass)

            if associations != "":
                dotContent += ("\nedge [arrowhead = open]\n")
                dotContent += associations

        # inheritances
        if self._drawInheritances:
            inheritances = ""
            for key, aClass in self.classes.items():
                inheritances += self._genInheritances(aClass)

            if inheritances != "":
                dotContent += ("\nedge [arrowhead = empty]\n")
                dotContent += inheritances

        dotContent += "}\n"
        return dotContent
