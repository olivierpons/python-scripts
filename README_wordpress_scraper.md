# wordpress_scraper.py

## English

### WordPress Authenticated Page Scraper

This script connects to a website, handles complex login forms with CSRF tokens,
and retrieves the HTML source code of a protected page. It is highly
configurable via a YAML file or command-line arguments.

**Features:**

- Authenticates on websites (like WordPress) with complex login forms.
- Automatically handles CSRF tokens by parsing the login page.
- Configuration can be provided via a YAML file, command-line arguments, or a
  mix of both.
- Allows for custom HTTP headers to be sent with requests.
- Robust error handling for various network issues (timeouts, SSL errors, etc.).
- Verbosity levels for detailed logging of the process.

**Usage:**

```bash
# Using a config file
python wordpress_scraper.py --config config.yaml

# Using command-line arguments
python wordpress_scraper.py --url <URL> --username <USER> --password <PASS> \
    --target-url <TARGET_URL>
```

**Arguments:**

- `-c, --config`: Path to the YAML configuration file.
- `-u, --url`: Base URL of the website.
- `--username`: Login username.
- `--password`: Login password.
- `-t, --target-url`: Full URL of the protected page to fetch.
- `-v, --verbosity`: Verbosity level: 0=silent, 1=normal, 2=verbose.

## Français

### Scraper de Page Authentifiée WordPress

Ce script se connecte à un site web, gère des formulaires de connexion complexes
avec des jetons CSRF, et récupère le code source HTML d'une page protégée. Il
est hautement configurable via un fichier YAML ou des arguments en ligne de
commande.

**Fonctionnalités :**

- S'authentifie sur des sites web (comme WordPress) avec des formulaires de
  connexion complexes.
- Gère automatiquement les jetons CSRF en analysant la page de connexion.
- La configuration peut être fournie via un fichier YAML, des arguments en
  ligne de commande, ou un mélange des deux.
- Permet d'envoyer des en-têtes HTTP personnalisés avec les requêtes.
- Gestion robuste des erreurs pour divers problèmes réseau (timeouts, erreurs
  SSL, etc.).
- Niveaux de verbosité pour un suivi détaillé du processus.

**Utilisation :**

```bash
# Avec un fichier de configuration
python wordpress_scraper.py --config config.yaml

# Avec des arguments en ligne de commande
python wordpress_scraper.py --url <URL> --username <USER> --password <PASS> \
    --target-url <URL_CIBLE>
```

**Arguments :**

- `-c, --config` : Chemin vers le fichier de configuration YAML.
- `-u, --url` : URL de base du site web.
- `--username` : Nom d'utilisateur pour la connexion.
- `--password` : Mot de passe pour la connexion.
- `-t, --target-url` : URL complète de la page protégée à récupérer.
- `-v, --verbosity` : Niveau de verbosité : 0=silencieux, 1=normal, 2=détaillé.

## 日本語

### WordPress認証ページスクレイパー

このスクリプトはウェブサイトに接続し、CSRFトークンを含む複雑なログインフォームを
処理して、保護されたページのHTMLソースコードを取得します。YAMLファイルまたは
コマンドライン引数により、高度な設定が可能です。

**機能：**

- 複雑なログインフォームを持つウェブサイト（WordPressなど）で認証します。
- ログインページを解析してCSRFトークンを自動的に処理します。
- 設定はYAMLファイル、コマンドライン引数、またはその両方の組み合わせで提供
  できます。
- リクエストでカスタムHTTPヘッダーを送信できます。
- 様々なネットワーク問題（タイムアウト、SSLエラーなど）に対する堅牢なエラー
  処理。
- プロセスの詳細なロギングのための詳細レベル。

**使用法：**

```bash
# 設定ファイルを使用
python wordpress_scraper.py --config config.yaml

# コマンドライン引数を使用
python wordpress_scraper.py --url <URL> --username <ユーザー> \
    --password <パスワード> --target-url <ターゲットURL>
```

**引数：**

- `-c, --config`：YAML設定ファイルへのパス。
- `-u, --url`：ウェブサイトのベースURL。
- `--username`：ログインユーザー名。
- `--password`：ログインパスワード。
- `-t, --target-url`：取得する保護されたページの完全なURL。
- `-v, --verbosity`：詳細レベル：0=静か、1=通常、2=詳細。

## 简体中文

### WordPress认证页面抓取器

此脚本连接到网站，处理带有CSRF令牌的复杂登录表单，并检索受保护页面的HTML
源代码。它可以通过YAML文件或命令行参数进行高度配置。

**功能：**

- 在具有复杂登录表单的网站（如WordPress）上进行身份验证。
- 通过解析登录页面自动处理CSRF令牌。
- 配置可以通过YAML文件、命令行参数或两者的混合方式提供。
- 允许随请求发送自定义HTTP标头。
- 对各种网络问题（超时、SSL错误等）进行稳健的错误处理。
- 提供详细级别的日志记录以跟踪过程。

**使用方法：**

```bash
# 使用配置文件
python wordpress_scraper.py --config config.yaml

# 使用命令行参数
python wordpress_scraper.py --url <网址> --username <用户名> \
    --password <密码> --target-url <目标网址>
```

**参数：**

- `-c, --config`: YAML配置文件的路径。
- `-u, --url`: 网站的基础URL。
- `--username`: 登录用户名。
- `--password`: 登录密码。
- `-t, --target-url`: 要抓取的受保护页面的完整URL。
- `-v, --verbosity`: 详细级别：0=静默，1=正常，2=详细。

## 繁體中文

### WordPress認證頁面擷取器

此腳本連接到網站，處理帶有CSRF權杖的複雜登入表單，並擷取受保護頁面的HTML
原始碼。它可通過YAML檔案或命令列參數進行高度配置。

**功能：**

- 在具有複雜登入表單的網站（如WordPress）上進行身份驗證。
- 通過解析登入頁面自動處理CSRF權杖。
- 可通過YAML檔案、命令列參數或兩者的混合方式提供配置。
- 允许隨請求發送自訂HTTP標頭。
- 對各種網路問題（超時、SSL錯誤等）進行穩健的錯誤處理。
- 提供詳細級別的日誌記錄以跟踪過程。

**使用方法：**

```bash
# 使用設定檔
python wordpress_scraper.py --config config.yaml

# 使用命令列參數
python wordpress_scraper.py --url <網址> --username <使用者名稱> \
    --password <密碼> --target-url <目標網址>
```

**參數：**

- `-c, --config`: YAML設定檔的路徑。
- `-u, --url`: 網站的基礎URL。
- `--username`: 登入使用者名稱。
- `--password`: 登入密碼。
- `-t, --target-url`: 要擷取的受保護頁面的完整URL。
- `-v, --verbosity`: 詳細級別：0=靜默，1=正常，2=詳細。

## Español

### Scraper de Páginas Autenticadas de WordPress

Este script se conecta a un sitio web, maneja formularios de inicio de sesión
complejos con tokens CSRF y recupera el código fuente HTML de una página
protegida. Es altamente configurable a través de un archivo YAML o argumentos
de línea de comandos.

**Características:**

- Se autentica en sitios web (como WordPress) con formularios de inicio de
  sesión complejos.
- Maneja automáticamente los tokens CSRF analizando la página de inicio de
  sesión.
- La configuración se puede proporcionar a través de un archivo YAML, argumentos
  de línea de comandos o una mezcla de ambos.
- Permite enviar encabezados HTTP personalizados con las solicitudes.
- Manejo robusto de errores para diversos problemas de red (tiempos de espera,
  errores SSL, etc.).
- Niveles de verbosidad para un registro detallado del proceso.

**Uso:**

```bash
# Usando un archivo de configuración
python wordpress_scraper.py --config config.yaml

# Usando argumentos de línea de comandos
python wordpress_scraper.py --url <URL> --username <USUARIO> \
    --password <CONTRASEÑA> --target-url <URL_OBJETIVO>
```

**Argumentos:**

- `-c, --config`: Ruta al archivo de configuración YAML.
- `-u, --url`: URL base del sitio web.
- `--username`: Nombre de usuario para el inicio de sesión.
- `--password`: Contraseña para el inicio de sesión.
- `-t, --target-url`: URL completa de la página protegida a obtener.
- `-v, --verbosity`: Nivel de verbosidad: 0=silencioso, 1=normal, 2=detallado.

## Italiano

### Scraper di Pagine Autenticate WordPress

Questo script si connette a un sito web, gestisce moduli di login complessi con
token CSRF e recupera il codice sorgente HTML di una pagina protetta. È
altamente configurabile tramite un file YAML o argomenti da riga di comando.

**Funzionalità:**

- Si autentica su siti web (come WordPress) con moduli di login complessi.
- Gestisce automaticamente i token CSRF analizzando la pagina di login.
- La configurazione può essere fornita tramite un file YAML, argomenti da riga
  di comando o un mix di entrambi.
- Consente di inviare header HTTP personalizzati con le richieste.
- Gestione robusta degli errori per vari problemi di rete (timeout, errori SSL,
  ecc.).
- Livelli di verbosità per un logging dettagliato del processo.

**Utilizzo:**

```bash
# Usando un file di configurazione
python wordpress_scraper.py --config config.yaml

# Usando argomenti da riga di comando
python wordpress_scraper.py --url <URL> --username <UTENTE> \
    --password <PASSWORD> --target-url <URL_TARGET>
```

**Argomenti:**

- `-c, --config`: Percorso del file di configurazione YAML.
- `-u, --url`: URL di base del sito web.
- `--username`: Nome utente per il login.
- `--password`: Password per il login.
- `-t, --target-url`: URL completo della pagina protetta da recuperare.
- `-v, --verbosity`: Livello di verbosità: 0=silenzioso, 1=normale, 2=dettagliato.

## Deutsch

### Scraper für authentifizierte WordPress-Seiten

Dieses Skript stellt eine Verbindung zu einer Website her, behandelt komplexe
Anmeldeformulare mit CSRF-Token und ruft den HTML-Quellcode einer geschützten
Seite ab. Es ist über eine YAML-Datei oder Befehlszeilenargumente hochgradig
konfigurierbar.

**Funktionen:**

- Authentifiziert sich auf Websites (wie WordPress) mit komplexen
  Anmeldeformularen.
- Behandelt CSRF-Token automatisch durch Parsen der Anmeldeseite.
- Die Konfiguration kann über eine YAML-Datei, Befehlszeilenargumente oder eine
  Mischung aus beidem bereitgestellt werden.
- Ermöglicht das Senden benutzerdefinierter HTTP-Header mit Anfragen.
- Robuste Fehlerbehandlung für verschiedene Netzwerkprobleme (Timeouts,
  SSL-Fehler usw.).
- Ausführlichkeitsstufen für eine detaillierte Protokollierung des Prozesses.

**Verwendung:**

```bash
# Verwendung einer Konfigurationsdatei
python wordpress_scraper.py --config config.yaml

# Verwendung von Befehlszeilenargumenten
python wordpress_scraper.py --url <URL> --username <BENUTZER> \
    --password <PASSWORT> --target-url <ZIEL_URL>
```

**Argumente:**

- `-c, --config`: Pfad zur YAML-Konfigurationsdatei.
- `-u, --url`: Basis-URL der Website.
- `--username`: Anmeldebenutzername.
- `--password`: Anmeldepasswort.
- `-t, --target-url`: Vollständige URL der geschützten Seite, die abgerufen
  werden soll.
- `-v, --verbosity`: Ausführlichkeitsstufe: 0=leise, 1=normal, 2=ausführlich.
