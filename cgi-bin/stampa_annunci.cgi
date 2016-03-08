#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use Switch;
use XML::LibXML;

my $cgi=new CGI;


my $session = CGI::Session->load();
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Annunci.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my @annuncio_titolo=$doc->findnodes("Annunci/Annuncio/Titolo/text()");
my @annuncio_data=$doc->findnodes("Annunci/Annuncio/Data/text()");
my @annuncio_testo=$doc->findnodes("Annunci/Annuncio/Testo/text()");
my @annuncio_immagine=$doc->findnodes("Annunci/Annuncio/Immagine/text()");

my $file='annunci_temp.html';
my $tot;
for (my $index=0; $index <=$#annuncio_titolo; $index++)
{	
	
	my $x='<div id="info-container"> <h3>'."@annuncio_titolo[$index]".'</h3>';
	$tot=$tot.$x;
	my $x='<div class="info-text"><p>'."@annuncio_data[$index]".'</p>';
	$tot=$tot.$x;
	my $x="<p>@annuncio_testo[$index]".'<p>';
	$tot=$tot.$x;
	my $x='<img src='."@annuncio_immagine[$index]".' alt='."Immagine annuncio".'></div></div>';
	$tot=$tot.$x;
}

my $lista_annunci="<ul>"."$tot"."</ul>";

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'lista_annunci' => $lista_annunci,
	};
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();