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
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?stampa_acquisto');
}
print $cgi->header('text/html');

my $amministratore=$session->param("amministratore");
my $email=$session->param("email");
my $pagamento=param("mpagamento-select");

my $parser=XML::LibXML->new;
my $carrello_doc=$parser->parse_file("../data/Carrelli.xml");
my $parser2=XML::LibXML->new;
my $prodotto_doc=$parser2->parse_file("../data/Prodotti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
my $indi=param('indirizzo');

my $num_prodotti=$carrello_doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");
my $tot_prodotto=0;
my $tot;
for(my $i=1; $i<=$num_prodotti; $i++)
{
	my @cod=$carrello_doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$i]/Prodotto/text()");
	my $codice=@cod[0]->string_value;
	my $x='<li><input type="hidden" name="prodotto'."$i".'" value="'."$codice".'"/></li>';
	$tot=$tot.$x;
	my @prz=$prodotto_doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Prezzo/text()");
	my $prezzo=@prz[0]->string_value;
	$tot_prodotto=$tot_prodotto+$prezzo;
	
}



my $x='<li><h2>Resoconto</h2></li>';
$tot=$tot.$x;

my $x='<li class="resocontoLi"><p>Prezzo totale: '."$tot_prodotto ".'&#8364;</p></li>';
$tot=$tot.$x;


my $x='<li class="resocontoLi"><p>Hai scelto l&#180;indirizzo numero: '."$indi".'</p></li>';
$tot=$tot.$x;

my $x='<li class="resocontoLi"><p>Metodo scelto: ';
$tot=$tot.$x;

if($pagamento eq 'carta_credito')
{
	my $x='Carta di credito</p></li>';
	$tot=$tot.$x;
	my $x='<li class="resocontoLi" ><label for="codice" >* Inserire codice: </label><div class="inputLeft"></div><div class="inputMiddle"><input id="codice" class="input" type="text" title="inserisci il codice" name="codice"/></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
}
elsif($pagamento eq 'bonifico')
{
	my $x='Bonifico</p></li>';
	$tot=$tot.$x;
	my $x='<li class="resocontoLi"><p>Le nostre coordinate bancarie sono: IT	11	X	03268	10001	100000000000</p></li>';
	$tot=$tot.$x;
}
elsif($pagamento eq 'contrassegno')
{
	my $x='Contrassegno</p></li>';
	$tot=$tot.$x;
	my $x='<li class="resocontoLi"><p>Le invieremo una mail con data e ora di arrivo previsto della merce</p></li>';
	$tot=$tot.$x;
}
elsif($pagamento eq 'pay_pal')
{
	my $x='Pay pal</p></li>';
	$tot=$tot.$x;
	my $x='<li class="resocontoLi"><label>* Inserire codice: </label><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="codice"/></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
}
elsif($pagamento eq 'carta_prepagata')
{
	my $x='Carta prepagata</p></li>';
	$tot=$tot.$x;
	my $x='<li class="resocontoLi"><label>* Inserire codice: </label><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="codice"/></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
}
my $x='<li>I campi con * sono obbligatori</li>';
$tot=$tot.$x;

my $x='<li><button class="button" type="submit" value="conferma">Conferma</button></li>';
$tot=$tot.$x;

my $lista_acquisto='<div class="generic-container"><div class="form-container2"><form action="aggiungi-ordine.cgi" method="post"><ul><li><input type="hidden" name="mpagamento" value="'."$pagamento".'"/><input type="hidden" name="indirizzo" value="'."$indi".'"/></li>'."$tot".'</ul></form></div></div>';

my $vars={
	'sessione' => "true",
	'email' => $email,
	'lista_acquisto' => $lista_acquisto,
	'amministratore'=>$amministratore,
	'messaggio_errore'=>'false',
};

my $file='resoconto_temp.html';
$template->process($file,$vars) || die $template->error();
