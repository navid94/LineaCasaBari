#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use XML::LibXML;
use Template;

my $cgi=new CGI;
print $cgi->header('text/html');

my @errors=();
my %values;

foreach my $p (param())
{
	$values{$p}=param($p);
}

my $pwd=$values{"password"};
foreach my $chiave (keys %values)
{
	if (!$values{$chiave})
	{
		push @errors, "Devi completare il campo '$chiave'.";
	}
	if ($chiave eq "email")
	{
		#controlli sul campo email
		if (!$values{$chiave}=~ /^[^ ,@]+\@([a-z0-9-]+\.)+[a-z]+$/)
		{
			push @errors, "Indirizzo email inserito non valido.";
		}
	}
	if ($chiave eq "password")
	{
		#controlli sul campo password
		
	}
	if ($chiave eq "conf_password")
	{
		if ($values{$chiave} ne $pwd)
		{
			push @errors, "La conferma della password non corrisponde.";
		}
	}
}

if (@errors)
{
=pod
	open(FORM,"../public_html/registrazione.html") or die $!;
	my $form=join('',<FORM>);
	close(FORM);
	my $error_message="<ul>"."<li>[@errors]</li>"."</ul>";
	$form=~ s/<!--error_message-->/$error_message/;
	my $original_css='<link href="LineaCasaBari.css" rel="stylesheet" type="text/css" media="screen"/>';
	my $correct_css='<link href="../LineaCasaBari.css" rel="stylesheet" type="text/css" media="screen"/>';
	$form=~ s/$original_css/$correct_css/;
	my $original_jquery='<script type="text/javascript" src="jquery-1.12.0.js"></script>';
	my $correct_jquery='<script type="text/javascript" src="../jquery-1.12.0.js"></script>';
	$form=~ s/$original_jquery/$correct_jquery/;
	my $original_linkskipper='<script type="text/javascript" src="link_skipper.js"></script>';
	my $correct_linkskipper='<script type="text/javascript" src="../link_skipper.js"></script>';
	$form=~ s/$original_linkskipper/$correct_linkskipper/;
	print $form;
=cut
	my $file='registrazione_temp.html';
	my $vars={
		'error' => "<ul>"."<li>[@errors]</li>"."</ul>"
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	if (-e "../data/Utenti.xml")
	{
		my $parser=XML::LibXML->new();
		my $doc=$parser->parse_file("../data/Utenti.xml");
		my $root=$doc->documentElement();
		my $utente_tag=$doc->createElement("Utente");
		$root->appendChild($utente_tag);
		my @value_tags=("Nome","Cognome","Email","Password");
		foreach my $k (@value_tags)
		{
			my $value_tag=$doc->createElement($k);
			$value_tag->appendTextNode($values{lc $k});
			$utente_tag->appendChild($value_tag);
		}
		my $indirizzo=$doc->createElement("Indirizzo");
		$utente_tag->appendChild($indirizzo);
		my @indirizzo_tags=("Via","Numero_civico","Città","Provincia","CAP");
		foreach my $x (@indirizzo_tags)
		{
			my $indirizzo_tag=$doc->createElement($x);
			$indirizzo->appendChild($indirizzo_tag);
		}
		my @novalue_tags=("Telefono","Amministratore");
		foreach my $i (@novalue_tags)
		{
			my $novalue_tag=$doc->createElement($i);
			if ($i eq "Amministratore")
			{
				$novalue_tag->appendTextNode("false");
			}
			$utente_tag->appendChild($novalue_tag);
		}
		open(XML,">","../data/Utenti.xml");
		print XML $doc->toString();
		close(XML);
	}
	else
	{
		my $doc=XML::LibXML::Document->new("1.0","UTF-8");
		my $root=$doc->createElement("Utenti");
		$doc->setDocumentElement($root);
		my $utente_tag=$doc->createElement("Utente");
		$root->appendChild($utente_tag);
		my @value_tags=("Nome","Cognome","Email","Password");
		foreach my $k (@value_tags)
		{
			my $value_tag=$doc->createElement($k);
			$value_tag->appendTextNode($values{lc $k});
			$utente_tag->appendChild($value_tag);
		}
		my $indirizzo=$doc->createElement("Indirizzo");
		$utente_tag->appendChild($indirizzo);
		my @indirizzo_tags=("Via","Numero_civico","Città","Provincia","CAP");
		foreach my $x (@indirizzo_tags)
		{
			my $indirizzo_tag=$doc->createElement($x);
			$indirizzo->appendChild($indirizzo_tag);
		}
		my @novalue_tags=("Telefono","Amministratore");
		foreach my $i (@novalue_tags)
		{
			my $novalue_tag=$doc->createElement($i);
			if ($i eq "Amministratore")
			{
				$novalue_tag->appendTextNode("false");
			}
			$utente_tag->appendChild($novalue_tag);
		}
		open (XML,">","../data/Utenti.xml");
		print XML $doc->toString();
		close(XML);
	}	
}
