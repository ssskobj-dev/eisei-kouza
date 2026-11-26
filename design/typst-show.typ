#show: doc => article(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(kouza-book)$
  book: true,
$endif$
$if(kouza-print)$
  print: true,
$endif$
$if(kouza-tagline)$
  tagline: [$kouza-tagline$],
$endif$
$if(kouza-edition)$
  edition: [$kouza-edition$],
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(papersize)$
  paper: "$papersize$",
$endif$
$if(mainfont)$
  font: ("$mainfont$",),
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
  doc,
)
