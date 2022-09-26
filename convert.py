import sys, re
import argparse
import subprocess
from markdownify import markdownify

def edit(filename, title, categories, tags):
  filepath = f"./_jupyter/{filename}.md"
  yaml = f"---\ntitle: {str(title)}\ncategories: {str(categories)}\ntags: {str(tags)}\n---\n\n"
  with open(filepath, 'r') as file:
    filedata = file.read()

  filedata = re.sub(r"!\[png\]\(", "<img src=\"/assets/images/", filedata)
  filedata = re.sub(".png\)", ".png\">", filedata)
  filedata = re.sub("""<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">""",'<div class="table-wrapper">\n<table>', filedata)
  filedata = re.sub('style="text-align: right;"', '', filedata)
  filedata = yaml + filedata
  with open(filepath, 'w') as file:
    file.write(filedata)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--filename', type=str)
  parser.add_argument('-t', '--title', type=str)
  parser.add_argument('-c', '--categories', type=str, nargs='*')
  parser.add_argument('-tg', '--tags', type=str, nargs='*')

  args = parser.parse_args()

  # convert .ipynb to .md
  filepath = f"./_jupyter/{args.filename}.ipynb"
  subprocess.call(f'jupyter nbconvert --to markdown {filepath}'.split(' '))

  # edit .md file for posting
  edit(args.filename,
       args.title,
       args.categories,
       args.tags)

  # move .md file to _posts dir
  subprocess.call(f'mv -f {filepath.replace("ipynb","md")} ./_posts/'.split(' '))
  # move images files to /assets/images dir
  subprocess.call(f'mv -f {filepath.replace(".ipynb","_files")} ./assets/images/'.split(' '))
  print("[Info] Conversion Complete!")
