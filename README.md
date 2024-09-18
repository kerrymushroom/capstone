# capstone

It's the capstone repository of the project **"An User-Customized Data Visualization System Based on Chat2VIS"**.

IEEE page: https://ieeexplore.ieee.org/document/10121440





**Three default folders:**

**/document:** Use this folder to save all meeting, resource, and reference documents.

**/project:** This is the code folder of our true project.

**/testout:** You can put your test code here.



**Three default branches:**

**/dev:** Our latest develop environment code, make a new push once a tiny independent module have been done. 

**Push to this branch only!**

* **Merge** and make sure you solved all the conflict agian before a new push.
* Remember to test your code agian after a merge.

```
#Prerequisites

git branch #To check your local branch
git checkout dev       #Switch to dev if you are not here

# Pull agian before a new push
git pull origin dev

# A push operation
git add .
git commit -m 'Your comments: write clearly what you have modified.'
git push -u origin dev
```



**/test:** Our test environment. It'll be cloned from dev branch once we get a new milestone.

**/main:** Our production environment. We will submit this version to school.

*You can create your own branch if you want **based on /dev branch**.*
