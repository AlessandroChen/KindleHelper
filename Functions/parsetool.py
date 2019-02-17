import os, stat

def addPermission(Filename):
    os.chmod(Filename, os.stat(Filename).st_mode | stat.S_IXUSR);

def transform(content):
    name = '';
    for i in range(0, len(content)):
        if (content[i] == ' ' and content[i + 1] == ' '):
            name += '\n';
        else:
            name += content[i];
    return name;

def getContent(name):
    j = 0;
    for i in range(0, len(name)):
        if name[i:i+7] == 'content':
            j = i + 9;
            for j in range(i + 9, len(name)):
                if (name[j] == "'" or name[j] == '"'):
                    break;
            return name[i+9:j];
