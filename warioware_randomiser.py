import argparse, shutil, random, os, zipfile

def main(src, dest, count):
  print("Source directory: %s" % src)
  print("Destination directory: %s" % dest)
  print("Number of files to copy: %d" % count)

  files = glob_files_randomly(src, count)
  random.shuffle(files)

  rom_group = files[:len(files)//2]
  sav_group = files[len(files)//2:]

  rom_path = os.path.join(dest, 'ROM')
  sav_path = os.path.join(dest, 'sav')

  if os.path.exists(rom_path) or os.path.exists(sav_path):
    print ("One or more of %s and %s already exist." % (rom_path, sav_path))
    exit()

  print("\nCOPYING:")

  copy_files(src, rom_group, rom_path)
  copy_files(src, sav_group, sav_path)

  print("\nCHANGING EXTENSIONS:")

  change_extension_dir(rom_path)
  change_extension_dir(sav_path)

  print("\nUNZIPPING:")

  unzip_dir(rom_group, rom_path)
  unzip_dir(sav_group, sav_path)

def glob_files_randomly(src, count):
  return random.sample(list(os.listdir(src)), count)

def copy_files(src, filenames, dest):
  os.makedirs(dest)
  for fname in filenames:
    srcpath = os.path.join(src, fname)
    shutil.copyfile(srcpath, os.path.join(dest, fname))
    print("File %s copied to %s" % (fname, dest))

def change_extension_dir(directory):
  filenames = list(os.listdir(directory))
  for fname in filenames:
    if not fname.startswith('.'):
      stripped = os.path.splitext(fname)[0] + '.zip'
      os.rename(
          os.path.join(directory, fname),
          os.path.join(directory, stripped)
      )
      print("File %s renamed to %s" % (fname, stripped))

def unzip_dir(group, path)
  for fname in group:
    if fname.endswith('.zip'):
      abs_path = os.path.join(path, fname)
      zip_ref = zipfile.ZipFile(abs_path)
      zip_ref.extractall(path)
      zip_ref.close()
      os.remove(abs_path)
      print("File %s unzipped" % fname)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Pick a random quantity WarioWare game files and move them to a target directory as .zip files')

  parser.add_argument('--src', action='store', dest='src', required=True,
                      help='The first source file directory (required)')
  parser.add_argument('--dest', action='store', dest='dest', required=True,
                      help='The destination directory for all modified files (required)')
  parser.add_argument('--count', action='store', dest='count', required=True,
                      help='The number of files to copy from the source directory (required)')

  args = parser.parse_args()


  main(args.src, args.dest, int(args.count))

