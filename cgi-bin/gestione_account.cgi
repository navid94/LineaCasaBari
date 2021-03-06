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
if ($session->is_empty) 
{
	if( $ENV{'QUERY_STRING'} eq 'mod')
	{
		print $cgi->redirect('check_session.cgi?gestione_account_mod');
	}
	elsif( $ENV{'QUERY_STRING'} ne 'exit')
	{
		print $cgi->redirect('check_session.cgi?gestione_account_normal');
	}
}

my $email=$session->param("email");
my $amministratore=$session->param("amministratore");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Utenti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my $old_name=$doc->findnodes("Utenti/Utente[Email='$email']/Nome/text()");
my $old_surname=$doc->findnodes("Utenti/Utente[Email='$email']/Cognome/text()");
my $old_tel=$doc->findnodes("Utenti/Utente[Email='$email']/Telefono/text()");

my $old_em_form='<input title="Inserire email" class="input" type="text" name="nuova_email" value="'."$email".'"/>';
my $old_name_form='<input title="Inserire nome" class="input" type="text" name="nuovo_nome" value="'."$old_name".'"/>';
my $old_surname_form='<input title="Inserire cognome" class="input" type="text" name="nuovo_cognome" value="'."$old_surname".'"/>';
my $old_tel_form='<input title="Inserire telefono" class="input" type="text" name="nuovo_telefono" value="'."$old_tel".'"/>';


my $vars;
my $file;
if($ENV{'QUERY_STRING'} eq 'ok')
{
			$vars={
					'log' => "Login effettuato con successo",
					'sessione' => "true",
					'email' => $email,
					'amministratore' => $amministratore,
					'vemail'=>$old_em_form,
					'vnome'=>$old_name_form,
					'vcognome'=>$old_surname_form,
					'vtelefono'=>$old_tel_form,	
				};
	$file='impostazioni_account_temp.html';
}
elsif ($ENV{'QUERY_STRING'} eq 'exit')
{
			$vars={
					'log' => "Logout effettuato con successo",
					'sessione' => "false",
					'email' => $email,
					'amministratore' => $amministratore,
					'vemail'=>$old_em_form,
					'vnome'=>$old_name_form,
					'vcognome'=>$old_surname_form,
					'vtelefono'=>$old_tel_form,
				};
				$file='login_temp.html';
}
elsif ($ENV{'QUERY_STRING'} eq 'mod')
{
	$vars={
			'sessione' => "true",
			'email' => $email,
			'amministratore' => $amministratore,
			'vemail'=>$old_em_form,
			'vnome'=>$old_name_form,
			'vcognome'=>$old_surname_form,
			'vtelefono'=>$old_tel_form,
			'log' =>"Modifica effettuata con successo",		
		};
		$file='impostazioni_account_temp.html';
}
else
{
	$vars={
			'sessione' => "true",
			'email' => $email,
			'amministratore' => $amministratore,
			'vemail'=>$old_em_form,
			'vnome'=>$old_name_form,
			'vcognome'=>$old_surname_form,
			'vtelefono'=>$old_tel_form,		
		};
		$file='impostazioni_account_temp.html';
}
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();
