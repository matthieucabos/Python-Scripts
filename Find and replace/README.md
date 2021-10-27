# Find and replace

****************************************

**Author** *CABOS Matthieu*

**Date** *2018*

**Organisation** *CEMES-CNRS*


****************************************

## Description

This algorithm used in a command line allow to edit raw source files and replace any par to another.

It will substitute a part of code by another, specifying the extension of the source code.

****************************************

 **WARNING !!! NO WAY BACK !!! , please be extremely careful**

****************************************

 The algorithm replace parts of codes into a source code.  
 
 The replaced code could be single word or a sequence.    
 
 In case of sequence please replace the full line to keep file structure .
 
 To treat big packages including differents levels of tree, the algorithm is recursive and will act on each .ext file.
 
 Please to use preserving the syntax :
 
 ```bash
 python3 find_and_replace.py 'py' 'for i in' 'for j in'
 
 python3 find_and_replace.py <Extension> <Code to replace> <Replacement Code>
 ```
 Where :
 * **Extension** is given as the first argument               
 * **Original code** to replace is given as the second one       
 * **Replacement code** is given as the third.  
 
 Those three arguments are given as string values.                      

Explanations:                                             
=============                                             
* -Create directory list and .py file list from current directory                                          
* -Rebuild original string path for each source file        
* -Open and replace the original code samples givenby the replace part of code                           
* -Write modified contents in source file     

****************************************

## Support

For any support request, please to mail @ matthieu.cabos@umontpellier.fr
