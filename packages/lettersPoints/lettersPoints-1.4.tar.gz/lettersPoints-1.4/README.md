This package is useful to generate points that, when plotted, form letters. The only function is write_text(), and it works with the following parameters:

write_text(string, height, distance_between_points, symbol_spacing = None, line_spacing = None, rotateAroundCenter = 0, filename = None):

	string - the text meant to be plotted, can be of any length; the accepted symbols are A-Z, 0-9, !, ?, and \n. All lowercase letters are converted to uppercase.

	height - the height that the symbols should have; all symbols are of width 0.4*height, except ! - than one has width 0.2*height

	distance_between_points - the distance between the points that will be generated

	symbol_spacing - the distance between symbols; if None, it will be set to height/10

	line_spacing - the distance between lines; if None, it will be set to height/10

	rotateAroundCenter - the angle by which the symbols should be rotated around their center point

	filename - a string; this will be the name of the csv output file (you don't have to add the .csv extension in the name); default value is None, and for that no output file is generated