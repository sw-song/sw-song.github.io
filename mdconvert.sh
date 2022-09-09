file_name=$1
title=$2
categories=$3
tags=$4


function run(){
  jupyter nbconvert --to markdown $file_name
  python convert.py ${file_name%.ipynb}.md ${title} ${categories} ${tags}
  mv ${file_name%.ipynb}.md ../_posts/
  mv ${file_name%.ipynb}_files ../assets/images/
  echo "============Conversion Complete!==========="
}

run
