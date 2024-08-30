-- MySQL dump 10.13  Distrib 5.7.33, for Linux (aarch64)
--
-- Host: localhost    Database: scalar_system
-- ------------------------------------------------------
-- Server version	5.7.33-0ubuntu0.18.04.1

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

-- Create user and the database

CREATE DATABASE scalar_system;
USE scalar_system;
CREATE USER 'scal_user'@'localhost' IDENTIFIED BY 'tH@r@236';
GRANT ALL PRIVILEGES ON scalar_system.* TO 'scal_user'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

--
-- Table structure for table `first_lookup`
--
DROP TABLE IF EXISTS `first_lookup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `first_lookup` (
  `vehicle_no` varchar(20) DEFAULT NULL,
  `customer` varchar(50) DEFAULT NULL,
  `product` varchar(30) DEFAULT NULL,
  `plant_no` varchar(10) DEFAULT NULL,
  `driver` varchar(50) DEFAULT NULL,
  `operator` varchar(50) DEFAULT NULL,
  UNIQUE KEY `vehicle_no` (`vehicle_no`,`customer`,`product`,`plant_no`,`driver`,`operator`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `first_lookup`
--

LOCK TABLES `first_lookup` WRITE;
/*!40000 ALTER TABLE `first_lookup` DISABLE KEYS */;
INSERT INTO `first_lookup` VALUES ('','','','','',''),('1234567890','123456789012345678901234567890','123456789012345678901234567890','1232456789','123456789012345678901234567890','123456789012345678901234567890'),('1234567890','d','d','1234567890','',''),('55-6589','fdfd','rice','','',''),('CAR1234','test1','test','2','test','test'),('CAR1578','Bil Bil','Bil Bil products','1','Crabby','Test'),('hh-0001','nimal','rice','2','kamla','namal'),('hh-0001','nimal','rice','3','kamal','namal'),('hh-0002','nimal','rice','1','kamal','sunil'),('hh-0003','ranil','rice','1','kamal','samal'),('hh-0003','ranil','rice','1','ranul','samal'),('hh-0003','saman','rice','3','sunil','nimal'),('hh-0006','k','k','k','k','k'),('hh-0020','rim','rice','2','nul','ml'),('hh-0099','km','kk','kk','kk','kk'),('hh-0111','k','k','k','k','k'),('hh-0905','kamal','rice','3','nal','mal'),('hh-0907','nimal','rcie','2','su','ka'),('hh-0909','kal','rice','2','nil','mul'),('hh-0981','kal','rice','3','nul','al'),('hh-0987','sunil','rice','1','nimal','niaml'),('hh-0988','kamal','rice','3','nimal','sunil'),('hh-0990','ranil','rice','2','sunil','lal'),('hh-1010','sunil','rice','1','nal','sul'),('hh-8899','sunil','rice','1','kamal','ranil'),('hh-8899','sunil','rice','2','kamal','ranil'),('hh-9088','nimal','rice','7','sunil','namal'),('hh-9944','nul','rice','2','sul','kal'),('hy-00001','namal','rice','1','kamla','sunil'),('hy-00002','namal','rice','1','kamla','sunil'),('kk-0001','kamal','rice','1','sunil','nimal'),('kk-0001','sunil','rice','1','lal','nil'),('kk-0002','kamal','rice','1','nimal','sunil'),('kk-0003','sunil','rice','1','lal','nil'),('kk-0004','sunil','rice','1','lal','nil'),('kk-0009','kamal','rice','1','kamal','sunil'),('kk-0086','kamal','rice','1','kamla','nimal'),('kk-0089','kamal','rice','1','kamla','nimal'),('kk-0091','kamla','rice','2','nim','sun'),('kk-0095','kamla','rice','2','nim','sun'),('kk-0099','sunil','rice','1','lal','nil'),('kk-8800','kamal','rice','1','kai','nui'),('rr-0987','trddf','eee','2','rty','4');
/*!40000 ALTER TABLE `first_lookup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `first_ticket`
--

DROP TABLE IF EXISTS `first_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `first_ticket` (
  `ticket_no` int(6) DEFAULT NULL,
  `first_datetime` datetime DEFAULT NULL,
  `vehicle_no` varchar(10) DEFAULT NULL,
  `customer` varchar(30) DEFAULT NULL,
  `product` varchar(30) DEFAULT NULL,
  `plant_no` varchar(10) DEFAULT NULL,
  `driver_name` varchar(30) DEFAULT NULL,
  `operator_name` varchar(30) DEFAULT NULL,
  `cx_field_1` varchar(30) DEFAULT NULL,
  `cx_field_2` varchar(30) DEFAULT NULL,
  `first_weight` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `first_ticket`
--

LOCK TABLES `first_ticket` WRITE;
/*!40000 ALTER TABLE `first_ticket` DISABLE KEYS */;
INSERT INTO `first_ticket` VALUES (100001,'2021-03-27 15:48:24','yy-0099','kamal','rice','1','kamla','kamla','','',48),(100001,'2021-03-27 15:48:29','yy-0099','kamal','rice','1','kamla','kamla','','',50),(100002,'2021-03-27 16:15:37','mn-0000','nimal','rice','1','nimal','nimal','','',51),(100002,'2021-03-27 16:15:42','mn-0000','nimal','rice','1','nimal','nimal','','',53),(100002,'2021-03-27 16:15:52','mn-0000','nimal','rice','1','nimal','nimal','','',46),(100003,'2021-03-27 16:17:32','pp-0000','nimal','rice','1','nimal','nimal','','',51),(100003,'2021-03-27 16:17:37','pp-0000','nimal','rice','1','nimal','nimal','','',53),(100004,'2021-03-27 16:29:16','yy-0000','nimal','rice','1','rice','kamla','','',54),(100004,'2021-03-27 16:29:28','yy-0000','nimal','rice','1','rice','kamla','','',47),(100004,'2021-03-27 16:34:12','yy-0000','nimal','rice','1','rice','kamla','','',47),(100004,'2021-03-27 16:34:17','yy-0000','nimal','rice','1','rice','kamla','','',49),(100004,'2021-03-27 16:34:22','yy-0000','nimal','rice','1','rice','kamla','','',51),(100004,'2021-03-27 16:34:30','yy-0000','nimal','rice','1','rice','kamla','','',53),(100004,'2021-03-27 16:34:30','yy-0000','nimal','rice','1','rice','kamla','','',53),(100004,'2021-03-27 16:37:45','yy-0011','nimal','rice','1','rice','kamla','','',52),(100005,'2021-03-27 16:41:59','jj-0000','kamal','rice','1','kamal','kamla','','',45),(100006,'2021-03-27 16:49:49','ii-0000','nimal','rice','1','nimal','nimal','','',54),(100007,'2021-03-27 16:53:40','ts-0000','namal','rice','2','namal','namal','','',52),(100007,'2021-03-27 16:53:51','ts-0000','namal','rice','2','namal','namal','','',45),(100007,'2021-03-27 16:54:44','ts-0001','namal','rice','2','namal','namal','','',50),(100008,'2021-03-27 16:59:31','jjj-0000','n','f','f','f','f','','',52),(100009,'2021-03-27 17:05:08','hh-0000','n','n','n','n','n','','',52),(100010,'2021-03-27 17:11:19','hh-0001','g','g','g','g','g','','',50),(100010,'2021-03-27 17:17:22','hh-0002','g','g','g','g','g','','',53),(100011,'2021-04-02 18:22:43','hh-0029','hamal','1','1','pathum','nimal','','',52),(100012,'2021-04-02 18:32:00','kk-0000','nimal','rice','1','kamla','ranil','','',45),(100013,'2021-04-02 18:32:51','kk-0001','rich','rice','1','driver','namal','','',50),(100014,'2021-04-02 18:50:27','hy-00001','namal','rice','1','kamla','sunil','','',50),(100014,'2021-04-02 18:52:10','hy-00002','namal','rice','1','kamla','sunil','','',53),(100014,'2021-04-02 18:52:50','hy-00002','namal','rice','1','kamla','sunil','','',47),(100014,'2021-04-02 18:52:55','hy-00002','namal','rice','1','kamla','sunil','','',49),(100014,'2021-04-02 18:53:15','hy-00002','namal','rice','1','kamla','sunil','','',55),(100015,'2021-04-02 19:00:41','hh-0001','nimal','rice','2','kamla','namal','','',47),(100016,'2021-04-02 19:02:44','hh-0001','nimal','rice','2','kamla','namal','','',52),(100017,'2021-04-03 10:42:57','hh-0003','ranil','rice','1','ranul','samal','','',48),(100018,'2021-04-03 10:45:17','hh-0002','nimal','rice','1','kamal','sunil','','',52),(100019,'2021-04-03 10:46:27','hh-0003','ranil','rice','1','kamal','samal','','',54),(100020,'2021-04-03 17:59:59','kk-0002','kamal','rice','1','nimal','sunil','','',49),(100021,'2021-04-03 18:18:59','hh-0002','nimal','rice','1','kamal','sunil','','',49),(100022,'2021-04-04 08:47:19','hh-0006','k','k','k','k','k','','',52),(100022,'2021-04-04 08:49:19','hh-0111','k','k','k','k','k','','',45),(100023,'2021-04-04 16:42:10','hh-0099','km','kk','kk','kk','kk','','',52),(100024,'2021-04-04 16:48:13','kk-0091','kamla','rice','2','nim','sun','','',52),(100024,'2021-04-04 16:50:50','kk-0095','kamla','rice','2','nim','sun','','',46),(100025,'2021-04-04 18:58:21','kk-0089','kamal','rice','1','kamla','nimal','','',52),(100025,'2021-04-04 19:01:51','kk-0086','kamal','rice','1','kamla','nimal','','',52),(100026,'2021-04-04 20:04:36','kk-8800','kamal','rice','1','kai','nui','','',54),(100027,'2021-04-11 16:38:12','hh-0988','kamal','rice','3','nimal','sunil','','',45),(100028,'2021-04-11 17:29:00','hh-0020','rim','rice','2','nul','ml','','',54),(100029,'2021-04-11 17:43:05','hh-0909','kal','rice','2','nil','mul','','',50),(100030,'2021-04-11 18:36:48','hh-0907','nimal','rcie','2','su','ka','','',54),(100031,'2021-04-11 19:08:45','hh-0905','kamal','rice','3','nal','mal','','',50),(100032,'2021-04-11 19:26:50','hh-0981','kal','rice','3','nul','al','','',54),(100033,'2021-04-11 19:33:46','hh-9944','nul','rice','2','sul','kal','','',47),(100033,'2021-04-11 19:37:53','hh-8899','sunil','rice','2','kamal','ranil','','',54),(100034,'2021-04-11 16:56:01','CAR1578','Bil Bil','Bil Bil products','1','Crabby','Test','','',46),(100035,'2021-04-11 16:53:21','CAR1234','test1','test','2','test','test','','',51),(100036,'2021-04-11 17:07:01','rr-0987','trddf','eee','2','rty','4','','',49),(100037,'2021-04-11 18:09:28','1234567890','123456789012345678901234567890','123456789012345678901234567890','1234567890','123456789012345678901234567890','123456789012345678901234567890','','',50),(100038,'2021-04-14 21:49:06','hh-0003','saman','rice','3','sunil','nimal','','',49),(100039,'2021-04-18 08:11:51','hh-0987','sunil','rice','1','nimal','niaml','','',48),(100040,'2021-04-18 13:48:07','55-6589','fdfd','rice','','','','','',2610),(100041,'2021-04-18 16:59:33','hh-0990','ranil','rice','2','sunil','lal','','',4),(100042,'2021-04-18 18:13:43','hh-0001','nimal','rice','3','kamal','namal','','',78);
/*!40000 ALTER TABLE `first_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `second_ticket`
--

DROP TABLE IF EXISTS `second_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `second_ticket` (
  `ticket_no` int(6) DEFAULT NULL,
  `first_datetime` datetime DEFAULT NULL,
  `second_datetime` datetime DEFAULT NULL,
  `vehicle_no` varchar(10) DEFAULT NULL,
  `customer` varchar(30) DEFAULT NULL,
  `product` varchar(30) DEFAULT NULL,
  `plant_no` varchar(10) DEFAULT NULL,
  `driver_name` varchar(30) DEFAULT NULL,
  `operator_name` varchar(30) DEFAULT NULL,
  `cx_field_1` varchar(30) DEFAULT NULL,
  `cx_field_2` varchar(30) DEFAULT NULL,
  `first_weight` double DEFAULT NULL,
  `second_weight` double DEFAULT NULL,
  `net_weight` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `second_ticket`
--

LOCK TABLES `second_ticket` WRITE;
/*!40000 ALTER TABLE `second_ticket` DISABLE KEYS */;
INSERT INTO `second_ticket` VALUES (100001,'2021-03-27 15:48:29','2021-03-27 15:49:14','yy-0099','kamal','rice','1','kamla','kamla','','',50,46,4),(100003,'2021-03-27 16:17:37','2021-03-27 16:18:01','pp-0000','nimal','rice','1','nimal','nimal','','',53,50,3),(100004,'2021-03-27 16:29:28','2021-03-27 16:29:57','yy-0000','nimal','rice','1','rice','kamla','','',47,46,1),(100006,'2021-03-27 16:49:49','2021-03-27 16:50:32','ii-0000','nimal','rice','1','nimal','nimal','','',54,46,8),(100007,'2021-03-27 16:54:44','2021-03-27 16:55:04','ts-0001','namal','rice','2','namal','namal','','',50,47,3),(100008,'2021-03-27 16:59:31','2021-03-27 17:01:00','jjj-0000','n','f','f','f','f','','',52,45,7),(100009,'2021-03-27 17:05:08','2021-04-02 18:30:04','hh-0000','n','n','n','n','n','','',52,45,7),(100010,'2021-03-27 17:11:19','2021-04-02 18:30:40','hh-0001','g','g','g','g','g','','',50,48,2),(100011,'2021-04-02 18:22:43','2021-04-02 18:31:30','hh-0029','hamal','1','1','pathum','nimal','','',52,46,6),(100014,'2021-04-02 18:50:27','2021-04-02 18:51:25','hy-00001','namal','rice','1','kamla','sunil','','',50,46,4),(100015,'2021-04-02 19:00:41','2021-04-02 19:01:59','hh-0001','nimal','rice','2','kamla','namal','','',47,45,2),(100016,'2021-04-02 19:02:44','2021-04-03 10:41:08','hh-0001','nimal','rice','2','kamla','namal','','',52,45,7),(100017,'2021-04-03 10:42:57','2021-04-03 10:43:22','hh-0003','ranil','rice','1','ranul','samal','','',48,45,3),(100010,'2021-03-27 17:17:22','2021-04-03 10:44:32','hh-0002','g','g','g','g','g','','',53,49,4),(100018,'2021-04-03 10:45:17','2021-04-03 10:45:37','hh-0002','nimal','rice','1','kamal','sunil','','',52,47,5),(100019,'2021-04-03 10:46:27','2021-04-03 10:46:52','hh-0003','ranil','rice','1','kamal','samal','','',54,51,3),(100013,'2021-04-02 18:32:51','2021-04-03 18:07:00','kk-0001','rich','rice','1','driver','namal','','',50,46,4),(100020,'2021-04-03 17:59:59','2021-04-03 18:09:55','kk-0002','kamal','rice','1','nimal','sunil','','',49,46,3),(100024,'2021-04-04 16:48:13','2021-04-04 16:49:51','kk-0091','kamla','rice','2','nim','sun','','',52,50,2),(100025,'2021-04-04 18:58:21','2021-04-04 19:00:46','kk-0089','kamal','rice','1','kamla','nimal','','',52,45,7),(100028,'2021-04-11 17:29:00','2021-04-11 17:30:07','hh-0020','rim','rice','2','nul','ml','','',54,46,8),(100033,'2021-04-11 19:33:46','2021-04-11 19:34:17','hh-9944','nul','rice','2','sul','kal','','',47,46,1),(100032,'2021-04-11 19:26:50','2021-04-11 19:35:11','hh-0981','kal','rice','3','nul','al','','',54,45,9),(100031,'2021-04-11 19:08:45','2021-04-11 19:35:46','hh-0905','kamal','rice','3','nal','mal','','',50,48,2),(100021,'2021-04-03 18:18:59','2021-04-11 19:36:06','hh-0002','nimal','rice','1','kamal','sunil','','',49,45,4),(100022,'2021-04-04 08:47:19','2021-04-11 19:36:21','hh-0006','k','k','k','k','k','','',52,51,1),(100023,'2021-04-04 16:42:10','2021-04-11 19:36:36','hh-0099','km','kk','kk','kk','kk','','',52,46,6),(100029,'2021-04-11 17:43:05','2021-04-11 19:37:01','hh-0909','kal','rice','2','nil','mul','','',50,45,5),(100030,'2021-04-11 18:36:48','2021-04-11 19:37:16','hh-0907','nimal','rcie','2','su','ka','','',54,51,3),(100034,'2021-04-11 16:56:01','2021-04-11 16:51:11','CAR1579','Bil Bil','Bil Bil products','1','Crabby','Test','','',46,45,1),(100035,'2021-04-11 16:53:21','2021-04-11 16:54:56','CAR1236','test1','test','2','test','test','','',51,45,6),(100037,'2021-04-11 18:09:28','2021-04-11 18:17:29','1234567890','123456789012345678901234567890','123456789012345678901234567890','1234567890','123456789012345678901234567890','123456789012345678901234567890','','',50,45,5),(100038,'2021-04-14 21:49:06','2021-04-14 21:49:56','hh-0003','saman','rice','3','sunil','nimal','','',49,47,2),(100039,'2021-04-18 08:11:51','2021-04-18 08:15:15','hh-0987','sunil','rice','1','nimal','niaml','','',48,46,2),(100040,'2021-04-18 13:48:07','2021-04-18 13:58:12','55-6589','fdfd','rice','','','','','',2610,1000,1610),(100027,'2021-04-11 16:38:12','2021-04-18 17:11:18','hh-0988','kamal','rice','3','nimal','sunil','','',45,56,11),(100041,'2021-04-18 16:59:33','2021-04-18 17:16:27','hh-0990','ranil','rice','2','sunil','lal','','',4,1,3),(100042,'2021-04-18 18:13:43','2021-04-18 18:15:12','hh-0001','nimal','rice','3','kamal','namal','','',78,44,34);
/*!40000 ALTER TABLE `second_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_setting`
--

DROP TABLE IF EXISTS `sys_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_setting` (
  `id` int(11) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `telephone` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `fax` varchar(200) DEFAULT NULL,
  `printer_format` varchar(10) DEFAULT NULL,
  `cx_field_1` varchar(200) DEFAULT NULL,
  `cx_field_2` varchar(200) DEFAULT NULL,
  `cx_field_1_inuse` tinyint(1) DEFAULT NULL,
  `cx_field_2_inuse` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_setting`
--

LOCK TABLES `sys_setting` WRITE;
/*!40000 ALTER TABLE `sys_setting` DISABLE KEYS */;
INSERT INTO `sys_setting` VALUES (1,'QUJDIENvbXBhbnkgUExD','Tm8uMSwgQSBSZCwgQSBDaXR5LCBTcmkgTGFua2E=','Kzk0MTExMTExLCAwMTIzNDU2Nzg5LCAwMTExMTEx','YWJjLmNvbXBhbnlAYWJjLmxr','Kzk0MTExMTExLCArOTQxMTExMjIy','Format-4','','',0,0);
/*!40000 ALTER TABLE `sys_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_user` (
  `user_name` varchar(30) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES ('admin','21232f297a57a5a743894a0e4a801fc3'),('operator','098f6bcd4621d373cade4e832627b4f6');
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_format`
--

DROP TABLE IF EXISTS `ticket_format`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket_format` (
  `format` varchar(10) DEFAULT NULL,
  `custom_info` varchar(500) DEFAULT NULL,
  `footer_info` varchar(500) DEFAULT NULL,
  `page_height` double DEFAULT NULL,
  `page_width` double DEFAULT NULL,
  `margin_left` double DEFAULT NULL,
  `margin_top` double DEFAULT NULL,
  `margin_right` double DEFAULT NULL,
  `margin_bottom` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_format`
--

LOCK TABLES `ticket_format` WRITE;
/*!40000 ALTER TABLE `ticket_format` DISABLE KEYS */;
INSERT INTO `ticket_format` VALUES ('Format-1','','dGVzdCBmb290ZXIgZm9ybWF0IC0gMQ==',5.5,9.5,1,0.5,1,0.5),('Format-2','','dGhhbmsgeW91IGZvcm1hdC0yIGNvbWUgYWdhaW4h',6.5,9.5,1,0.5,0.5,0.5),('Format-3','','eW91ciBzaWduYXR1cmUgaGVyZSBmb3JtYXQtMw==',9.5,9.5,1,0.5,1,0.5),('Format-4','','Y2hhbmdlZCB0ZXN0IGZvb3RlciBmb3JtYXRlIC0gNA==',5.5,9.5,1,0.5,1,0.5),('Report','','',11.69,8.27,0.5,1,0.5,1);
/*!40000 ALTER TABLE `ticket_format` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-27 20:16:09
