<!DOCTYPE html>
<!--Sample splash page-->
<head>
  <link href='style.css' rel='stylesheet' type='text/css'>
</head>

 <?php   
        /*Connexion à la base de données sur le serveur tp-epua*/
        $conn = @mysqli_connect("localhost", "root", "");    
        
        /*connexion à la base de donnée depuis la machine virtuelle INFO642*/
        /*$conn = @mysqli_connect("localhost", "etu", "bdtw2021");*/  

        if (mysqli_connect_errno()) {
            $msg = "erreur ". mysqli_connect_error();
        } else {  
            $msg = "connecté au serveur " . mysqli_get_host_info($conn);
            /*Sélection de la base de données*/
            mysqli_select_db($conn, "twitter_api"); 
            /*mysqli_select_db($conn, "etu"); */ /*sélection de la base sous la VM info642*/
        
            /*Encodage UTF8 pour les échanges avecla BD*/
            mysqli_query($conn, "SET NAMES UTF8");
        }
        
  ?>


<body class = "background">
  <div id="intro">
    <p><b>TWITTER</b></p>
    
    <navbar>
      <ul>
        <li>
          <a href="page_0.php">
            <p>Rapport</p>
          </a>
        </li>
        <li>
          <a href="map.html">
            <p>Map</p>
          </a>
        </li>
      </ul>
  </navbar>
</div>
<footer class="footer">
    
</footer>
</body>



</html>