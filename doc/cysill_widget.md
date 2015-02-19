# Ategyn Cysill Ar-lein

Fel rhan o ddarpariaeth yr API Cysill ar lein, rydym ni o techiaith.org wedi rhyddhau ategyn er mwyn integreiddio gwirydd sillafu a gramadeg o fewn eich wefan. Mae'r ategyn yma yn defnyddio API Cysill ar lein, ac felly mae'n enghraifft da o beth allwch chi gyflawni gyda'r API

Er mwyn integreiddio'r ategyn o fewn eich wefan, dilynwch y camau isod:

* Ychwanegwch dau tag `<script>` i cod tudalen eich gwefan. Un gyda'ch allwedd API, ac un i URL y sgript Cysill Ar-lein:
    
         <script>
                var CYSILL_API_KEY = "EICH_ALLWEDD_API";
         </script>
         <meta name="gwt:property" content="locale=cy" />
         <script type="text/javascript" language="javascript" src="https://api.techiaith.org/cysill/ui/CysillArlein/CysillArlein.nocache.js"></script>

    
* Ychwanegwch `<div>` gydag `id=CysillArleinApp` unrhywle o fewn eich tudalen 
    

         <div id="fy_nhudalen">
         <div id='CysillArleinApp'></div>
         </div>

* Dewisol: Steilio'r ategyn gan defnyddio'r dosbarthiadau `cysillwidget` a `cysilltextarea`:

        <style>
        /* Enghraiff o css */
        #fy_nhudalen {
            border:1px solid #000;
        }
         /* .cysillwidget: dosbarth sy'n cael ei 
         lapio o amgylch y widget cyfan */
         .cysillwidget {
             width: 500px;
             border: 1px solid #333;
             padding: 2px 20px 2px 2px;
             float:right;
         }
 
         /* .cysilltextarea: dosbarth sy'n cael ei lapio
         o amgylch y 'textarea' yn unig. Defnyddio'r 
         dosbarth yma e.e. ar gyfer setio uchder y
         textarea */
         .cysilltextarea {
             height:50px;
             font-size:12px;
         }
        </style>


---------

# Cysill Online Widget

As part of the Cysill API, we at techiaith.org have also released a widget for integrating a Welsh language and grammar checker into your website. This widget uses the Cysill API, and is therefore an example of the abilities of the API.

In order to integrate the widget into your website, follow these steps:

* Add two `<script>` tags to your website source code. The first with your Cysill API Key, and the 2nd with the URL of the Cysill Online source:
    
         <script>
                var CYSILL_API_KEY = "EICH_ALLWEDD_API";
         </script>
         <meta name="gwt:property" content="locale=cy" />
         <script type="text/javascript" language="javascript" src="https://api.techiaith.org/cysill/ui/CysillArlein/CysillArlein.nocache.js"></script>
    
* Add a `<div>` with `id=CysillArleinApp` anywhere on your page:
    
         <div id="my_body">
         <div id='CysillArleinApp'></div>
         </div>
    
* Optional: Style the widget using the CSS classes `cysillwidget` and `cysilltextarea`:

         <style>
         /* An example of some css */
             
             /* .cysillwidget is a class wrapped
             around the entire widget */
             .cysillwidget {
                 width: 500px;
                 border: 1px solid #333;
                 padding: 2px 20px 2px 2px;
                 float:right;
             }
             
             /* .cysilltextarea is a class wrapped around the 
             text area only. Use it, for example, to set the
             textarea height */
             .cysilltextarea {
                 height:50px;
                 font-size:12px;
             }
        </style>
        
