git submodule update --recursive --remote
rm external/how_phasors_work/myst.yml
cd external/ontario_electricity_market/ && git checkout version-for-blog && git reset --hard origin/version-for-blog && cd ../../ && git add external/ontario_electricity_market/
rm external/ontario_electricity_market/myst.yml
cd external/python-cluedo/ && git checkout for-blog && git reset --hard origin/for-blog && cd ../../ && git add external/python-cluedo/
cd external/bluegreen_resume_template/ && git checkout green-resume && git reset --hard origin/green-resume & cd ../../ && git add external/bluegreen_resume_template/

python3 -c '
import sys
with open("resume_template.md") as f:
    content = f.read()
with open("external/bluegreen_resume_template/populated_subtemplate.html") as f:
    populated_subtemplate = f.read()
REPLACEMENTS = [
    (">keeganmjgreen@gmail.com<", ">Email<"),
    (" <br> ", " "),
    ("<br>", " "),
]
for (old, new) in REPLACEMENTS:
    populated_subtemplate = populated_subtemplate.replace(old, new)
content = content.replace("<!-- subtemplate -->", populated_subtemplate)
with open("resume.md", "w") as f:
    f.write(content)
'
