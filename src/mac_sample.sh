python3 CodeDependencyVisualizer.py -aiptP --verbose -d /Users/Ricky/repo/github/CuraEngine/src -I /Users/Ricky/repo/github/CuraEngine/libs /Users/Ricky/repo/github/CuraEngine/src/modelFile /Users/Ricky/repo/github/CuraEngine/src/utils /Users/Ricky/repo/github/CuraEngine/src --includeClasses "cura::*"
dot -T pdf -o uml.pdf uml.dot
echo "open uml.pdf with Xpdf viewer"

