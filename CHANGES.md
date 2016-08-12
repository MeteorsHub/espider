# Espider Changelog

>You can see the full list of changes between each espider version.  

## version 0.1.2

- New espider mode -- update mode.  
  You can config espider to launch in 'update' mode or 'override' mode(original mode).  
  In this mode, every time you launch your project, espider will automatically compare new parsing data with the original and only save the ones that have changed.  
  If you want to use this mode, you should make your paser return an specific order of fields. For `re` user, see the 3rd changes.
- Fix some bugs:  
  * Now you can make your code more compact. Extraction with `re` can change the code from `re.findall(pattern, data)` to `re.findall(pattern, data)[0]` in order to avoid errors that may occur.  
  * The number of contentLimit in configs will show correctly when running project with its value set not 'inf'.  
- Now you can return OrderedDict in a list in your parser. The order of each field will save to file and database as the order in your defination.

## version 0.1.1

- Adding most of the code comments, README files.
- Begin to build docs that users could refer to.
- Fix some bugs.
- Optimize framework.

## version 0.1.0  

- First public version of espider.
- Build basic framework of espider.  
- Provide original functions.