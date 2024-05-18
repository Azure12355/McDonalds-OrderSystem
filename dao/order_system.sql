/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80034
 Source Host           : localhost:3306
 Source Schema         : order_system

 Target Server Type    : MySQL
 Target Server Version : 80034
 File Encoding         : 65001

 Date: 01/01/2024 14:52:36
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for coupon
-- ----------------------------
DROP TABLE IF EXISTS `coupon`;
CREATE TABLE `coupon`  (
  `coupon_id` int NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  `merchant_id` int NULL DEFAULT NULL,
  `coupon_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `discount_amount` decimal(10, 2) NULL DEFAULT NULL,
  `expiration_date` date NULL DEFAULT NULL,
  PRIMARY KEY (`coupon_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `merchant_id`(`merchant_id` ASC) USING BTREE,
  CONSTRAINT `coupon_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `coupon_ibfk_2` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`merchant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of coupon
-- ----------------------------
INSERT INTO `coupon` VALUES (1, 1, 1, '满减券', 5.00, '2024-01-15');
INSERT INTO `coupon` VALUES (2, 2, 2, '折扣券', 0.10, '2024-01-20');

-- ----------------------------
-- Table structure for delivery
-- ----------------------------
DROP TABLE IF EXISTS `delivery`;
CREATE TABLE `delivery`  (
  `delivery_id` int NOT NULL,
  `order_id` int NULL DEFAULT NULL,
  `delivery_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `delivery_person_id` int NULL DEFAULT NULL,
  `delivery_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`delivery_id`) USING BTREE,
  INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `delivery_person_id`(`delivery_person_id` ASC) USING BTREE,
  CONSTRAINT `delivery_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `ordertable` (`order_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `delivery_ibfk_2` FOREIGN KEY (`delivery_person_id`) REFERENCES `deliveryperson` (`delivery_person_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of delivery
-- ----------------------------
INSERT INTO `delivery` VALUES (1, 1, '配送地址1', 1, '已派送');
INSERT INTO `delivery` VALUES (2, 2, '配送地址2', 2, '配送中');

-- ----------------------------
-- Table structure for deliveryperson
-- ----------------------------
DROP TABLE IF EXISTS `deliveryperson`;
CREATE TABLE `deliveryperson`  (
  `delivery_person_id` int NOT NULL,
  `delivery_person_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `contact_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`delivery_person_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of deliveryperson
-- ----------------------------
INSERT INTO `deliveryperson` VALUES (1, '配送员1', '555-111-2222');
INSERT INTO `deliveryperson` VALUES (2, '配送员2', '555-333-4444');

-- ----------------------------
-- Table structure for dishcategory
-- ----------------------------
DROP TABLE IF EXISTS `dishcategory`;
CREATE TABLE `dishcategory`  (
  `category_id` int NOT NULL,
  `category_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`category_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dishcategory
-- ----------------------------
INSERT INTO `dishcategory` VALUES (1, '分类1');
INSERT INTO `dishcategory` VALUES (2, '分类2');

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `menu_id` int NOT NULL,
  `menu_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `category_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`menu_id`) USING BTREE,
  INDEX `category_id`(`category_id` ASC) USING BTREE,
  CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `dishcategory` (`category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, '菜单1', 1);
INSERT INTO `menu` VALUES (2, '菜单2', 2);

-- ----------------------------
-- Table structure for merchant
-- ----------------------------
DROP TABLE IF EXISTS `merchant`;
CREATE TABLE `merchant`  (
  `merchant_id` int NOT NULL,
  `merchant_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `merchant_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `merchant_contact` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `restaurant_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`merchant_id`) USING BTREE,
  INDEX `restaurant_id`(`restaurant_id` ASC) USING BTREE,
  CONSTRAINT `merchant_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of merchant
-- ----------------------------
INSERT INTO `merchant` VALUES (1, '商家1', '商家地址1', '111-222-3333', 1);
INSERT INTO `merchant` VALUES (2, '商家2', '商家地址2', '444-555-6666', 2);

-- ----------------------------
-- Table structure for ordertable
-- ----------------------------
DROP TABLE IF EXISTS `ordertable`;
CREATE TABLE `ordertable`  (
  `order_id` int NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  `merchant_id` int NULL DEFAULT NULL,
  `dish_id` int NULL DEFAULT NULL,
  `order_time` datetime NULL DEFAULT NULL,
  `order_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `merchant_id`(`merchant_id` ASC) USING BTREE,
  INDEX `dish_id`(`dish_id` ASC) USING BTREE,
  CONSTRAINT `ordertable_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ordertable_ibfk_2` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`merchant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ordertable_ibfk_3` FOREIGN KEY (`dish_id`) REFERENCES `menu` (`menu_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ordertable
-- ----------------------------
INSERT INTO `ordertable` VALUES (1, 1, 1, 1, '2024-01-03 18:45:00', '已下单');
INSERT INTO `ordertable` VALUES (2, 2, 2, 2, '2024-01-04 20:15:00', '已完成');

-- ----------------------------
-- Table structure for restaurant
-- ----------------------------
DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE `restaurant`  (
  `restaurant_id` int NOT NULL,
  `restaurant_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `restaurant_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `contact_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of restaurant
-- ----------------------------
INSERT INTO `restaurant` VALUES (1, '餐厅1', '地址1', '123-456-7890');
INSERT INTO `restaurant` VALUES (2, '餐厅2', '地址2', '987-654-3210');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int NOT NULL,
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `user_password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `user_email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '用户1', '密码1', 'user1@gmail.com', '111-222-3333');
INSERT INTO `user` VALUES (2, '用户2', '密码2', 'user2@gmail.com', '444-555-6666');

-- ----------------------------
-- Table structure for usermerchantlogin
-- ----------------------------
DROP TABLE IF EXISTS `usermerchantlogin`;
CREATE TABLE `usermerchantlogin`  (
  `record_id` int NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  `merchant_id` int NULL DEFAULT NULL,
  `login_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`record_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `merchant_id`(`merchant_id` ASC) USING BTREE,
  CONSTRAINT `usermerchantlogin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `usermerchantlogin_ibfk_2` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`merchant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of usermerchantlogin
-- ----------------------------
INSERT INTO `usermerchantlogin` VALUES (1, 1, 1, '2024-01-01 12:00:00');
INSERT INTO `usermerchantlogin` VALUES (2, 2, 2, '2024-01-02 14:30:00');

-- ----------------------------
-- Table structure for userreview
-- ----------------------------
DROP TABLE IF EXISTS `userreview`;
CREATE TABLE `userreview`  (
  `review_id` int NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  `merchant_id` int NULL DEFAULT NULL,
  `rating` int NULL DEFAULT NULL,
  `review_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `review_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`review_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `merchant_id`(`merchant_id` ASC) USING BTREE,
  CONSTRAINT `userreview_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `userreview_ibfk_2` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`merchant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userreview
-- ----------------------------
INSERT INTO `userreview` VALUES (1, 1, 1, 4, '好吃！', '2024-01-05 10:00:00');
INSERT INTO `userreview` VALUES (2, 2, 2, 5, '非常好！', '2024-01-06 11:30:00');

SET FOREIGN_KEY_CHECKS = 1;
