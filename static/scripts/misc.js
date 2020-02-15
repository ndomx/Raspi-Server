function deleteDirectory(dirpath)
{
    var msg = "Do you want to delete this folder?\nYou won't be able to undo this action";
    deletePath(dirpath, msg);
}

function deleteFile(filepath)
{
    var dirlist = filepath.split('/');
    var index = dirlist.length - 1;
    if (dirlist[index] == '')
    {
        index--;
    }

    var filename = dirlist[index];
    var msg = "Do you want to delete " + filename + "?\nYou won't be able to undo this action";

    deletePath(filepath, msg);
}

function deletePath(path, msg)
{
    var res = confirm(msg);
    if (res == true)
    {
        window.location.replace('/__delete__/'+path);
    }
}