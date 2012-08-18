divert(-1)dnl
#
# $Id: head.m4,v 1.1 2006/10/16 03:20:53 memmett Exp $
#

divert(0)dnl
ifelse(_php,`t',<?= '<?xml version="1.0"?>' ?>, `<?xml version="1.0"?>')
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1"/>
    <meta http-equiv="Content-Language" content="en"/>
    <title>_title</title>
    <meta name="description" lang="en" content="_description"/>
    <meta name="keywords" lang="en" content="_keywords"/>
    <meta name="author" content="_author"/>
    <link rev="made" href="mailto:_authoremail"/>
    <link rel="stylesheet" type="text/css" href="_stylesheet"/>
    <link href='http://fonts.googleapis.com/css?family=Droid+Serif' rel='stylesheet' type='text/css'>
    <script type="text/javascript"
      src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
  </head>
  <body>
    <a id="top"></a>

    <div id="content">
    <!-- content -->

    <!-- header -->
    <div id="header">
      <h1>_title</h1>
    </div>
    <!-- header -->

