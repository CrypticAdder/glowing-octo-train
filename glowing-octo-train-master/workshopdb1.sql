/*
 Navicat Premium Data Transfer

 Source Server         : 13COM
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : localhost:3306
 Source Schema         : workshopdb1

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 15/08/2019 10:36:16
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles`  (
  `RoleId` int(11) NOT NULL AUTO_INCREMENT,
  `RoleName` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`RoleId`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for tblworkshop
-- ----------------------------
DROP TABLE IF EXISTS `tblworkshop`;
CREATE TABLE `tblworkshop`  (
  `WorkshopId` int(11) NOT NULL,
  `Date` datetime(0) NULL DEFAULT NULL,
  `Room` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `Subject` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `Summary` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `Teachers` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `MaxStudents` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `OwnerId` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`WorkshopId`) USING BTREE,
  INDEX `OwnerId`(`OwnerId`) USING BTREE,
  CONSTRAINT `tblworkshop_ibfk_1` FOREIGN KEY (`OwnerId`) REFERENCES `users` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for tblworkshopasgn
-- ----------------------------
DROP TABLE IF EXISTS `tblworkshopasgn`;
CREATE TABLE `tblworkshopasgn`  (
  `Id` int(11) NOT NULL,
  `WorkshopId` int(11) NULL DEFAULT NULL,
  `UserId` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `WorkshopId`(`WorkshopId`) USING BTREE,
  INDEX `UserId`(`UserId`) USING BTREE,
  CONSTRAINT `tblworkshopasgn_ibfk_1` FOREIGN KEY (`WorkshopId`) REFERENCES `tblworkshop` (`WorkshopId`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tblworkshopasgn_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `users` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `Id` int(11) NOT NULL,
  `FirstName` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `LastName` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `RoleId` int(11) NULL DEFAULT NULL,
  `Email` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `Phone` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `Username` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NULL DEFAULT NULL,
  `Password` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `RoleId`(`RoleId`) USING BTREE,
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`RoleId`) REFERENCES `roles` (`RoleId`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'dev', 'dev', NULL, NULL, NULL, 'dev', 'dev');

SET FOREIGN_KEY_CHECKS = 1;
