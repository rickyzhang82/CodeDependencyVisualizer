python3 CodeDependencyVisualizer.py -aiptP --verbose -d /home/Ricky/repo/github/CuraEngine/src -I /home/Ricky/repo/github/CuraEngine/libs /home/Ricky/repo/github/CuraEngine/src/modelFile /home/Ricky/repo/github/CuraEngine/src/utils /home/Ricky/repo/github/CuraEngine/src --includeClasses "cura::*"
dot -T pdf -o uml.pdf uml.dot
echo "open uml.pdf with Xpdf viewer"

