// A file system object in the file system
// Every object has at most one parent
sig FSObject { parent: lone Dir }

// The set of directories in the file system
sig Dir extends FSObject { contents: set FSObject }

// The set of files in the file system
sig File extends FSObject { }

// There exists a unique root
one sig Root extends Dir { } { no parent }

//All file system objects are either files or directories
fact { File + Dir = FSObject }

// Every directory is the parent of each of  its contents
fact { all d: Dir, o: d.contents | o.parent = d }

// Property asserting a model has at least 3 Dirs and 3 Files
pred ismodel { #Dir>2 && #File>2 }

// Command to find a model of size at most 6
run ismodel for 6

// Comment out the above command to proceed futher

// Uncomment the fact below to implement the axiom that
// every file system object is in the hereditary contents of the root
// fact { all o: FSObject | o in Root.*contents }

// Check to see that file systems are acyclic
assert acyclic { no d: Dir | d in d.^contents }
check acyclic for 8

// This example is developed much further in the on-line Alloy tutorial:
// 	http://alloy.mit.edu/alloy/tutorials/online/

