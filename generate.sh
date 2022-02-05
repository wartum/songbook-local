#!/bin/sh -u

transformTxtFn()
{
	longest_line_length_int=$(awk -v max='0' -F '::' '\
		{
			sub("[ ]+$", "", $1)
			if (length($1)>max) max=length
		} END {print max}' "$1" )

	awk -v max="$longest_line_length_int" -F '::' '\
		{
			sub("[ ]+$", "", $1)
			sub("^[ ]+", "", $2)
			if (length($1) != 0)
				printf("%-*s::%s\n", max+5, $1, " " $2)
			else
				print ""
		}' "$1" > "$1.tmp"
	mv "$1.tmp" "$1"
}

createTexFn()
{
	title_str=$(echo "${1##*/}" | sed "s/.txt//")
	tex_file_name_str=$(echo "${title_str}.tex" | sed "s/ /_/g")
	tex_file_path_str="./songs/tex/${tex_file_name_str}"

	awk -F '::' -v title="$title_str" '\
		BEGIN {
			print "\\subsection{" title "}\n\n\\begin{tabular}{l l}\n"
		}
		{
			sub("[ ]+$", "", $1)
			sub("^[ ]+", "", $2)
			gsub("#", "\\#", $2)
			if (substr($1,1,1) == "+")
				print "\t\\textbf{" substr($1,2) "}";
			else if (substr($1,1,3) == "===")
				print "\t\\end{tabular}\n\t\\newpage\n\t\\begin{tabular}{l l}";
			else
				print "\t" $1;
			print "\t&" $2 "\\\\"
		}
		END {
			print "\\end{tabular}"
		}' "$1" > "$tex_file_path_str"
}

genSongsFn()
{
	for file_str in ./songs/workdir/*.txt; do
		transformTxtFn "$file_str"
		createTexFn "$file_str"
	done
}

getSongbookFn()
{
	inputs_str=""
	for tex_file_name_str in ./songs/tex/*.tex; do
		inputs_str="${inputs_str}\n\\\input{${tex_file_name_str#*/}}\n\\\newpage"
	done
	awk -v inputs="$inputs_str" '\
		{
			if ($0 == "-- Songs here --")
				print inputs
			else
				print
		}' "songbook.def.tex" > "songbook.tex"
}

genSongsFn
getSongbookFn

pdflatex songbook.tex
pdflatex songbook.tex
pdflatex songbook.tex
rm ./*.aux
rm ./*.log
rm ./*.toc
rm ./*.out
aws s3 cp songbook.pdf s3://piewoj/songbook.pdf
aws s3api put-object-tagging --bucket piewoj --key songbook.pdf --tagging 'TagSet={Key=public,Value=yes}'
