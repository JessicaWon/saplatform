-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: saltcmd
-- ------------------------------------------------------
-- Server version	5.1.73

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=58 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add user cmd',7,'add_usercmd'),(20,'Can change user cmd',7,'change_usercmd'),(21,'Can delete user cmd',7,'delete_usercmd'),(22,'Can add user host',8,'add_userhost'),(23,'Can change user host',8,'change_userhost'),(24,'Can delete user host',8,'delete_userhost'),(33,'Can delete user file',11,'delete_userfile'),(32,'Can change user file',11,'change_userfile'),(31,'Can add user file',11,'add_userfile'),(42,'Can delete salt update file',14,'delete_saltupdatefile'),(41,'Can change salt update file',14,'change_saltupdatefile'),(40,'Can add salt update file',14,'add_saltupdatefile'),(37,'Can add salt user file',13,'add_saltuserfile'),(38,'Can change salt user file',13,'change_saltuserfile'),(39,'Can delete salt user file',13,'delete_saltuserfile'),(57,'Can delete cloud server status',19,'delete_cloudserverstatus'),(56,'Can change cloud server status',19,'change_cloudserverstatus'),(55,'Can add cloud server status',19,'add_cloudserverstatus'),(53,'Can change game server',18,'change_gameserver'),(52,'Can add game server',18,'add_gameserver'),(54,'Can delete game server',18,'delete_gameserver');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$AtauHhglD5gp$t5E6JpDEX6FiGB7GZt9jlU2lBm+4T7FNkbC9HHrHMh8=',NULL,1,'root','','','',1,1,'2016-12-16 07:22:50');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','permission'),(3,'auth','group'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'mycmd','usercmd'),(8,'mycmd','userhost'),(11,'mycmd','userfile'),(14,'mycmd','saltupdatefile'),(13,'mycmd','saltuserfile'),(19,'mycmd','cloudserverstatus'),(18,'mycmd','gameserver');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-12-14 09:29:42'),(2,'auth','0001_initial','2016-12-14 09:29:42'),(3,'admin','0001_initial','2016-12-14 09:29:42'),(4,'contenttypes','0002_remove_content_type_name','2016-12-14 09:29:42'),(5,'auth','0002_alter_permission_name_max_length','2016-12-14 09:29:42'),(6,'auth','0003_alter_user_email_max_length','2016-12-14 09:29:42'),(7,'auth','0004_alter_user_username_opts','2016-12-14 09:29:42'),(8,'auth','0005_alter_user_last_login_null','2016-12-14 09:29:42'),(9,'auth','0006_require_contenttypes_0002','2016-12-14 09:29:42'),(10,'mycmd','0001_initial','2016-12-14 09:29:42'),(11,'sessions','0001_initial','2016-12-14 09:29:42'),(12,'mycmd','0002_userhost','2016-12-14 10:10:25'),(13,'mycmd','0003_userfile','2016-12-15 07:16:59'),(14,'mycmd','0004_auto_20161216_0300','2016-12-16 03:00:06'),(15,'mycmd','0005_delete_user','2016-12-16 03:11:57'),(16,'mycmd','0006_modelformwithfilefield_userfile','2016-12-19 03:15:13'),(17,'mycmd','0007_auto_20161219_1036','2016-12-19 10:36:18'),(18,'mycmd','0008_auto_20161220_0613','2016-12-20 06:13:48'),(19,'mycmd','0009_saltcreatenewgameserver_saltupdatefile_serverstatus','2016-12-24 07:20:42'),(20,'mycmd','0010_loginuser','2016-12-26 06:32:38'),(21,'mycmd','0011_delete_loginuser','2016-12-26 08:42:14'),(22,'mycmd','0012_auto_20161228_0800','2016-12-28 08:00:10'),(23,'mycmd','0013_auto_20161228_0801','2016-12-28 08:01:09'),(24,'mycmd','0014_auto_20161228_0815','2016-12-28 08:15:46'),(25,'mycmd','0015_auto_20170103_0711','2017-01-03 07:11:27'),(26,'mycmd','0016_auto_20170103_0853','2017-01-03 08:53:31');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mycmd_cloudserverstatus`
--

DROP TABLE IF EXISTS `mycmd_cloudserverstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mycmd_cloudserverstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_time` datetime NOT NULL,
  `server_ip` varchar(60) NOT NULL,
  `server_status` varchar(60) NOT NULL,
  `server_status_reason` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mycmd_cloudserverstatus`
--

LOCK TABLES `mycmd_cloudserverstatus` WRITE;
/*!40000 ALTER TABLE `mycmd_cloudserverstatus` DISABLE KEYS */;
INSERT INTO `mycmd_cloudserverstatus` VALUES (1,'2016-12-24 00:00:00','192.168.10.1','running','running'),(2,'2016-12-26 00:00:00','192.168.10.2','running','running'),(3,'2016-12-26 09:00:00','192.168.10.2','running','running'),(4,'2016-12-26 09:00:00','192.168.10.2','running','running'),(5,'2016-12-26 09:00:00','192.168.10.2','running','running'),(6,'2016-11-26 09:00:00','192.168.10.3','running','running'),(7,'2016-10-26 09:00:00','192.168.10.3','running','running'),(8,'2016-10-26 12:00:00','192.168.10.3','running','running'),(9,'2016-09-26 09:00:00','192.168.10.3','running','running'),(10,'2016-09-26 12:00:00','192.168.10.3','running','running'),(11,'2016-09-26 18:00:00','192.168.10.3','running','running');
/*!40000 ALTER TABLE `mycmd_cloudserverstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mycmd_gameserver`
--

DROP TABLE IF EXISTS `mycmd_gameserver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mycmd_gameserver` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `engineer_name` varchar(60) NOT NULL,
  `project_name` varchar(60) NOT NULL,
  `project_dir` varchar(60) NOT NULL,
  `gameserver_id` varchar(60) DEFAULT NULL,
  `cloud_server_eth0_ip` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mycmd_gameserver`
--

LOCK TABLES `mycmd_gameserver` WRITE;
/*!40000 ALTER TABLE `mycmd_gameserver` DISABLE KEYS */;
INSERT INTO `mycmd_gameserver` VALUES (1,'2016-09-28 09:00:00','2016-09-28 12:00:00','wangjuan','pkq','/root/server','gameserver4','192.168.10.2'),(2,'2016-09-28 09:00:00','2016-09-28 13:00:00','lijian','saierhao','/root/server','gameserver5','192.168.10.3'),(3,'2016-09-28 09:00:00','2016-09-28 14:00:00','liyuan','wulinwaizhuan','/srv/server','gameserver5','192.168.10.4'),(4,'2016-09-28 09:00:00','2016-09-28 12:00:00','liliangyi','pkq','/root/server','gameserver5','192.168.10.2'),(5,'2016-09-28 09:00:00','2016-10-28 12:00:00','liliangyi','pkq','/root/server','gameserver5','192.168.10.5'),(6,'2016-11-28 09:00:00','2016-11-28 12:00:00','liliangyi','pkq','/root/server','gameserver8','192.168.10.5'),(7,'2016-12-28 09:00:00','2016-12-28 12:00:00','liliangyi','pkq','/root/server','gameserver9','192.168.10.5'),(8,'2016-12-28 09:00:00','2016-12-28 12:00:00','liliangyi','pkq','/root/server','gameserver10','192.168.10.5'),(9,'2016-12-28 09:00:00','2016-12-28 12:00:00','liliangyi','pkq','/root/server','gameserver11','192.168.10.5'),(10,'2016-08-28 09:00:00','2016-08-28 12:00:00','liliangyi','pkq','/root/server','gameserver1','192.168.10.5'),(11,'2016-08-29 09:00:00','2016-08-28 12:00:00','liliangyi','pkq','/root/server','gameserver2','192.168.10.5'),(12,'2016-08-29 09:00:00','2016-08-28 12:00:00','liliangyi','pkq','/root/server','gameserver3','192.168.10.5'),(13,'2016-07-29 09:00:00','2016-07-28 12:00:00','liliangyi','wulinwaizhuan','/root/server','gameserver3','192.168.10.4'),(14,'2016-07-29 09:00:00','2016-07-28 12:00:00','liliangyi','wulinwaizhuan','/root/server','gameserver2','192.168.10.4'),(15,'2016-06-29 09:00:00','2016-06-29 12:00:00','liyuan','wulinwaizhuan','/root/server','gameserver2','192.168.10.4');
/*!40000 ALTER TABLE `mycmd_gameserver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mycmd_saltupdatefile`
--

DROP TABLE IF EXISTS `mycmd_saltupdatefile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mycmd_saltupdatefile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `engineer_name` varchar(60) NOT NULL,
  `upload_file` varchar(100) NOT NULL,
  `update_dir` varchar(60) NOT NULL,
  `project_name` varchar(60) NOT NULL,
  `project_dir` varchar(60) NOT NULL,
  `salt_command` varchar(60) NOT NULL,
  `salt_selected_gameserver` varchar(60) NOT NULL,
  `salt_outcome` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mycmd_saltupdatefile`
--

LOCK TABLES `mycmd_saltupdatefile` WRITE;
/*!40000 ALTER TABLE `mycmd_saltupdatefile` DISABLE KEYS */;
/*!40000 ALTER TABLE `mycmd_saltupdatefile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mycmd_saltuserfile`
--

DROP TABLE IF EXISTS `mycmd_saltuserfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mycmd_saltuserfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `upload_file` varchar(100) NOT NULL,
  `update_dir` varchar(60) NOT NULL,
  `salt_command` varchar(50) NOT NULL,
  `salt_host` varchar(50) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=58 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mycmd_saltuserfile`
--

LOCK TABLES `mycmd_saltuserfile` WRITE;
/*!40000 ALTER TABLE `mycmd_saltuserfile` DISABLE KEYS */;
INSERT INTO `mycmd_saltuserfile` VALUES (1,'upload/test222222222_nMKHek3.txt','/opt','salt-test-20161219','192.168.12.19','2016-12-20 06:13:48','2016-12-20 06:13:48'),(2,'upload/test222222222_qT9JnJY.txt','/opt','salt-test-201612201220','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(3,'upload/test222222222_vjuAnY7.txt','/opt','salt-test-201612201221','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(4,'upload/test222222222_Ble6o9g.txt','/opt','salt-test-201612201222','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(5,'upload/test222222222_sk4sO1A.txt','/opt','salt-test-201612201223','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(6,'upload/test222222222_raGAUZv.txt','/opt','salt-test-201612201151','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(7,'upload/test222222222_zQOhdmI.txt','/opt','salt-test-201612201151','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(8,'upload/test222222222_A7JrFHH.txt','/opt','salt-test-201612201220','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(9,'upload/test222222222_VEQv9Vb.txt','/opt','salt-test-201612201220','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(10,'upload/test222222222_UO4At5N.txt','/opt','salt-test-201612201220','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(11,'upload/test222222222_jCfQFde.txt','/opt','salt-test-201612201347','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(12,'upload/test222222222_xk7MB4C.txt','/opt','salt-test-201612201347','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(13,'upload/test222222222_zk8P1Vv.txt','/opt','salt-test-201612201347','192.168.12.20','2016-12-20 06:13:48','2016-12-20 06:13:48'),(14,'upload/test222222222_X353TVz.txt','/opt','test.ping','192.168.30.148','2016-12-20 06:13:48','2016-12-20 06:13:48'),(15,'upload/test222222222_OikJ3m0.txt','/opt','test.ping','192.168.30.148','2016-12-20 06:15:10','2016-12-20 06:15:10'),(16,'upload/test222222222_GRFfndS.txt','/opt','test.ping','192.168.30.148','2016-12-20 06:24:40','2016-12-20 06:24:40'),(17,'upload/test222222222_uFBm2aI.txt','/opt','test.ping','192.168.30.148','2016-12-20 06:27:13','2016-12-20 06:27:13'),(18,'upload/test11111111111_PrGECOC.txt','/opt','test.ping','192.168.30.148','2016-12-20 07:31:08','2016-12-20 07:31:08'),(19,'upload/test11111111111_Bwi9t8R.txt','/opt','salt.cp','192.168.1.3','2017-01-03 06:02:47','2017-01-03 06:02:47'),(20,'upload/test11111111111_nCm06TP.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 08:54:43','2017-01-03 08:54:43'),(21,'upload/test11111111111_6OyFvxt.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 08:58:15','2017-01-03 08:58:15'),(22,'upload/test11111111111_l7Hmnrz.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 08:59:55','2017-01-03 08:59:55'),(23,'upload/test11111111111_9EeUWWn.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:01:10','2017-01-03 09:01:10'),(24,'upload/test11111111111_PK31new.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:01:33','2017-01-03 09:01:33'),(25,'upload/test11111111111_SORedgG.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:01:43','2017-01-03 09:01:43'),(26,'upload/test11111111111_2fseMSd.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:02:22','2017-01-03 09:02:22'),(27,'upload/test11111111111_dsxAdkw.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:02:46','2017-01-03 09:02:46'),(28,'upload/test11111111111_RZ4GveJ.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:02:53','2017-01-03 09:02:53'),(29,'upload/test11111111111_TkzMdac.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:03:37','2017-01-03 09:03:37'),(30,'upload/test11111111111_dVx8qMJ.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:05:00','2017-01-03 09:05:00'),(31,'upload/test11111111111_c6a6yPn.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:05:05','2017-01-03 09:05:05'),(32,'upload/test11111111111_UPZgyMd.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:05:33','2017-01-03 09:05:33'),(33,'upload/test11111111111_AQgYJr9.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:16:19','2017-01-03 09:16:19'),(34,'upload/test11111111111_fGDV9Sg.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:16:46','2017-01-03 09:16:46'),(35,'upload/test11111111111_EbLtqRT.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:17:09','2017-01-03 09:17:09'),(36,'upload/test11111111111_tsxYLHB.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:42:54','2017-01-03 09:42:54'),(37,'upload/test11111111111_AcGjlbq.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:42:57','2017-01-03 09:42:57'),(38,'upload/test11111111111_UE5eFDc.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:43:09','2017-01-03 09:43:09'),(39,'upload/test11111111111_TTnORsm.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:43:11','2017-01-03 09:43:11'),(40,'upload/test11111111111_zywjKYA.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:43:41','2017-01-03 09:43:41'),(41,'upload/test11111111111_gRCDcq4.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:44:11','2017-01-03 09:44:11'),(42,'upload/test11111111111_e3yiNQA.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:44:43','2017-01-03 09:44:43'),(43,'upload/test11111111111_WciBtgm.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 09:44:45','2017-01-03 09:44:45'),(44,'upload/test11111111111_8Q2jokK.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 10:08:00','2017-01-03 10:08:00'),(45,'upload/test11111111111.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 10:16:14','2017-01-03 10:16:14'),(46,'upload/test11111111111.txt','/srv/salt/','salt.cp','192.168.1.3','2017-01-03 10:20:01','2017-01-03 10:20:01'),(47,'upload/test11111111111_HjGrtYS.txt','/opt','salt.cp','192.168.1.3','2017-01-03 10:20:54','2017-01-03 10:20:54'),(48,'upload/test11111111111_V11szAn.txt','/opt','salt.cp','192.168.1.3','2017-01-03 10:27:50','2017-01-03 10:27:50'),(49,'upload/test11111111111_dCQlO8A.txt','/opt','salt.cp','192.168.30.147','2017-01-03 10:28:23','2017-01-03 10:28:23'),(50,'upload/test11111111111_WK1pwaR.txt','/opt','salt.cp','192.168.30.147','2017-01-03 10:28:58','2017-01-03 10:28:58'),(51,'upload/test11111111111_TueE1YL.txt','/opt','salt.cp','192.168.30.147','2017-01-03 10:29:31','2017-01-03 10:29:31'),(52,'upload/test11111111111_dZaEHiX.txt','/opt','salt.cp','192.168.30.147','2017-01-03 10:33:35','2017-01-03 10:33:35'),(53,'upload/test11111111111_3w91bIu.txt','/opt','salt.cp','192.168.30.147','2017-01-03 10:33:39','2017-01-03 10:33:39'),(54,'upload/test11111111111_XBCQt9w.txt','/opt','salt.cp','192.168.1.3','2017-01-03 10:34:37','2017-01-03 10:34:37'),(55,'upload/test11111111111_YiPDr10.txt','/opt','cp.get_file','192.168.30.147','2017-01-04 02:27:49','2017-01-04 02:27:49'),(56,'upload/test11111111111_VEKzlhp.txt','/opt','cp.get_file','192.168.30.148','2017-01-04 06:01:36','2017-01-04 06:01:36'),(57,'upload/test11111111111.txt','/opt','cp.get_file','192.168.30.148','2017-01-04 06:09:55','2017-01-04 06:09:55');
/*!40000 ALTER TABLE `mycmd_saltuserfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mycmd_usercmd`
--

DROP TABLE IF EXISTS `mycmd_usercmd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mycmd_usercmd` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `u_cmd` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mycmd_usercmd`
--

LOCK TABLES `mycmd_usercmd` WRITE;
/*!40000 ALTER TABLE `mycmd_usercmd` DISABLE KEYS */;
INSERT INTO `mycmd_usercmd` VALUES (1,'test.ping'),(2,'test2.ping'),(3,'salt'),(4,'salt'),(5,'salt'),(6,'salt'),(7,''),(8,''),(9,'salt12191358'),(10,''),(11,''),(12,''),(13,''),(14,'salt12161125'),(15,''),(16,''),(17,''),(18,''),(19,''),(20,''),(21,'salt12191551');
/*!40000 ALTER TABLE `mycmd_usercmd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mycmd_userfile`
--

DROP TABLE IF EXISTS `mycmd_userfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mycmd_userfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `f_title` varchar(30) NOT NULL,
  `u_file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mycmd_userfile`
--

LOCK TABLES `mycmd_userfile` WRITE;
/*!40000 ALTER TABLE `mycmd_userfile` DISABLE KEYS */;
INSERT INTO `mycmd_userfile` VALUES (1,'11111111111','upload/test11111111111_axqrzlB.txt'),(2,'11111111111','upload/test11111111111_El2LRUi.txt'),(3,'11111111111','upload/test222222222.txt'),(4,'11111111111','upload/test222222222_pPccHGi.txt'),(5,'1111111111122','upload/test11111111111_DHduxrE.txt'),(6,'11111111111','upload/test222222222_okUzVyH.txt');
/*!40000 ALTER TABLE `mycmd_userfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mycmd_userhost`
--

DROP TABLE IF EXISTS `mycmd_userhost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mycmd_userhost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `u_host` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mycmd_userhost`
--

LOCK TABLES `mycmd_userhost` WRITE;
/*!40000 ALTER TABLE `mycmd_userhost` DISABLE KEYS */;
INSERT INTO `mycmd_userhost` VALUES (1,'192.168.1.1'),(2,'192.168.1.1'),(3,'192.168.1.1'),(4,'192.168.1.1'),(5,''),(6,''),(7,'192.168.1.1'),(8,''),(9,''),(10,''),(11,''),(12,'192.168.1.1'),(13,''),(14,''),(15,''),(16,''),(17,''),(18,''),(19,'192.168.1.1');
/*!40000 ALTER TABLE `mycmd_userhost` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-01-09 10:28:08
