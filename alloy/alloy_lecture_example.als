// A file system object in the file system
sig FSObject { parent: lone Dir }

// A directory in the file system
sig Dir extends FSObject { contents: set FSObject }

// A file in the file system
sig File extends FSObject { }

// There exists a root
one sig Root extends Dir { } { no parent }

//All file system objects are either files or directories
fact { File + Dir = FSObject }

// Every directory is the parent of each of  its contents
fact { all d: Dir, o: d.contents | o.parent = d }

// Every file system object is in the hereditary contents of the root
fact { all o: FSObject | o in Root.*contents }

// Existence of a model with 3 Dirs and 3 Files
pred ismodel [] {
	#Dir>2 && #File>2
} run ismodel for 6

// Check to see that file systems are acyclic
assert acyclic { no d: Dir | d in d.^contents }
check acyclic for 6

// This example is developed much further in the on-line Alloy tutorial:
// 	http://alloy.mit.edu/alloy/tutorials/online/

