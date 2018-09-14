* latest update: 2/10/2018

* gets the csv files gathered from the python code;
* returns a file named names which contains all of them;
* saves it in raw_thez.names;
* only keeping matches 40 and 50;

dm 'clear log';

%let list = 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016;
%let path = C:\Users\mhaghbaali1\OneDrive for Business\New Thesis\Data\;

%macro test;
	%do i = 1 %to %sysfunc(countw(&list));
		* read the year;
		%let year = %scan(&list,&i); 
		* define the file path;
		%let filepath = &path.out&year..csv;
		* check;
		%put &filepath;
		
		* import the csv files into sas;
		data out&year;
			%let _EFIERR_ = 0; /* set the ERROR detection macro variable */
			infile "&filepath"
 			delimiter = ';' MISSOVER DSD lrecl = 32767 ;
  		    informat VAR1 $250. ;
  			informat VAR2 $250. ;
  			informat VAR3 $250. ;
  			format VAR1 $250. ;
  			format VAR2 $250. ;
  			format VAR3 $250. ;
  			input
  				VAR1 $
  			    VAR2 $
  			    VAR3 $;
				if _ERROR_ then call symputx('_EFIERR_',1);  /* set ERROR detection macro variable */
		run;
		
		data out&year;
			set out&year;
			rename
				var1 = address
				var2 = name
				var3 = found;
		run;

		data out&year;
			set out&year;
			if found = 'Full Match' then
				check = 1;
			else
				check = 0; 
		run;

		/*
		%let outerfile = &path.sas&year..csv;

		proc export data = out&year outfile = "&outerfile" dbms=dlm replace;
			delimiter = ';';
		run;
		*/

		data out&year (drop = i h len j k);
			length fname $ 250 mname $ 250 lname $ 250 found $ 250 
				   ffname $ 250 fmname $ 250 flname $ 250; 

			retain name fname lname mname address ffname flname fmname found check;
			set out&year;
			* set the length for mname;

			len = countw(name);
			*find first name and last name;
			lname = scan(name,len);
			fname = scan(name,1);
			mname = '';
			* everything in between is middle name;
			if len > 2 then do;
				do i = 2 to (len - 1);
					h = scan(name,i);
					mname = left(cats(compress(mname),h));
				end;
			end;

			* do  the same thing for the found names; 
			flen = countw(found);
			*find first name and last name;
			flname = scan(found,flen);
			ffname = scan(found,1);
			fmname = '';
			* everything in between is middle name;
			if flen > 2 then do;
				do j = 2 to (len - 1);
					k = scan(found,j);
					fmname = left(cats(compress(fmname),k));
				end;
			end;
		run;
			* how to accept a match or not;
		data out&year;
			set out&year;

			* if the found name is only one word, it is not acceptable;
			if flen = 1 then delete;

			* if it is a full match, I count it;
			if check = 1 then 
				match = 50;
			* very similar to a full match;
			else if (compress(fname) = compress(ffname)) and (compress(lname) = compress(flname)) and (compress(mname) = compress(fmname)) then
				match = 40;
			* lower levels of matching;
			* because some mnames have a lenghth of zero, it will produce errors, but noting important;
			else if (compress(fname) = compress(ffname)) and (compress(lname) = compress(flname)) and (substr(compress(mname),1,1) = substr(compress(fmname),1,1)) then
				match = 30;
			else if (compress(fname) = compress(ffname)) and (compress(lname) = compress(flname)) and (compress(mname) = '') and (compress(fmname) ~= '') then
				match = 25;
			else if (compress(fname) = compress(ffname)) and (compress(lname) = compress(flname)) and (compress(mname) ~= '') and (compress(fmname) = '') then
				match = 20;
			* no match at all;
			else 
				match = 0;
	
			* most of words with more than 3 words are not correct, may be one or two;
			if flen > 3 and match > 0 then delete;
			* deleting the non-matches;
			if match = 0 then delete;
		run;

		*%uniques(out&year, name match);
		
		proc sort data = out&year noduplicate;
			by name address;
		run;

		* add variable year for concating;
		data out&year;
			set out&year;
			year = &year;
		run;

	%end;
		* add all datasets together;
		data names;
			set out: ;
			drop check flen;
		run;
%mend;
%test;

proc datasets noprint;
	delete out2003-out2016;
run;

data names2;
	set names;
	if match in (40,50);
run;

data raw_thez.names2;
	set names2;
run;
