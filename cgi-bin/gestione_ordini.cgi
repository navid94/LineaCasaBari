#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;

my $session = CGI::Session->load();
my $email=$session->param("email");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my $new_codice=param("Codice");
my $new_utente=param("Utente");
my $new_cod=param("Data");



print $cgi->header('text/html');
print param("Prodotto1");
