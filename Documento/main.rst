.. role:: cite

.. raw:: latex

   \providecommand*\DUrolecite[1]{\cite{#1}}


.. role:: ref

.. raw:: latex

   \providecommand*\DUroleref[1]{\ref{#1}}


.. raw:: LaTeX

	  %----------------------------------------------------------------------------
	  \frontmatter
	  %----------------------------------------------------------------------------
	  \pagestyle{fancy}

	  \pdfbookmark[1]{Indice General}{Indice General}

	  \parskip2pt        				                    % space between paragraphs

	  \tableofcontents                                      % Table of contents

	  \listoffigures                                        % List of figures

  	  \pdfbookmark[1]{Indice de Figuras}{Indice de Figuras}

	  \listoftables                                         % List of tables

	  \pdfbookmark[1]{Indice de Cuadros}{Indice de Cuadros}

	%$docinfo


	 %----------------------------------------------------------------------------
	  \mainmatter
	 %----------------------------------------------------------------------------

.. include:: 01-introduccion.rst

.. include:: 02-descripcionGeneral.rst

.. include:: 03-marcoteorico.rst

.. include:: 04-desarrollometodologico.rst

.. include:: 05-analisis.rst

.. include:: 06-conclusiones.rst

.. raw:: latex

	\backmatter

	\bibliographystyle{apacite}

	% argument is your BibTeX string definitions and bibliography database(s)
	\bibliography{bibl}

        \addcontentsline{toc}{chapter}{Anexos}
