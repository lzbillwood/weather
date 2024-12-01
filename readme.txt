…or create a new repository on the command line

echo "# LDA" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:lzbillwood/LDA.git
git push -u origin main

…or push an existing repository from the command line

git remote add origin git@github.com:lzbillwood/LDA.git
git branch -M main
git push -u origin main

ssh-keygen -t rsa -b 4096 -C "48832347@qq.com"

git add requirements.txt

git commit -m "更新 requirements.txt 文件"

git push origin main
