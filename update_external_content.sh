git submodule update --recursive --remote
rm external/how_phasors_work/myst.yml
cd external/ontario_electricity_market/ && git checkout version-for-blog && git reset --hard origin/version-for-blog && cd ../../ && git add external/ontario_electricity_market/
rm external/ontario_electricity_market/myst.yml
cd external/python-cluedo/ && git checkout for-blog && git reset --hard origin/for-blog && cd ../../ && git add external/python-cluedo/
