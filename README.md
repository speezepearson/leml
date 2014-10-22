LEML
====

Lightweight extensible markup language

Motivation
==========

I often want to embed plots, directed graphs, or math-typeset stuff in my documents, and I resent needing to carry the image files around separately from the text. If a resource has a concise text representation, I should be able to embed that representation in the text file in the first place, and "compile" it to HTML or something, and the compilation process will use the text resource-descriptions to generate the resources and embed them appropriately in the output.

I like LaTeX's math typesetting and Markdown's backtick's for code; I want the best of both worlds, and I want more than that. I want this:

	 Here's some inline math: $x$
	 Here's some block math:  $$ \int_0^1 f(x) \,dx $$
	 Here's some inline code: `A[0]`
	 Here's a directed graph: {{digraph: on -> off; off -> on;}}
	 Here's a plot:           {{plot: xs=arange(10); ys=xs**2; scatter(xs, ys)}}

         <compile the above to HTML; get>

	 Here's some inline math: <img src="latex-x.png" />
	 Here's some block math:  <p><img src="latex-int_0_1_f_x_dx.png" /></p>
	 Here's some inline code: <code>A[0]</code>
	 Here's a directed graph: <p><img src="dot_on_off.png" /></p>
	 Here's a plot:           <p><img src="plot_01.png" /></p>

LEML can do this, and LEML can do more. If you want to embed blaggles in your document, and you have a Python function or a shell script that creates a blaggle given a text representation of the blaggle, it is trivially easy to extend LEML to create/embed blaggles.