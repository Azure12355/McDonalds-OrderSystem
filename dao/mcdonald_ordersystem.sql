/*
 Navicat Premium Data Transfer

 Source Server         : Azure-MySQL
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44-log)
 Source Host           : localhost:3306
 Source Schema         : mcdonald_ordersystem

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44-log)
 File Encoding         : 65001

 Date: 11/06/2024 16:47:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for affordable_packages
-- ----------------------------
DROP TABLE IF EXISTS `affordable_packages`;
CREATE TABLE `affordable_packages`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img_path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `simplified_title` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `price` double NULL DEFAULT NULL,
  `discount` decimal(10, 2) NULL DEFAULT 0.00,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of affordable_packages
-- ----------------------------
INSERT INTO `affordable_packages` VALUES (1, '../res/McDonald_packages/JumboBreakfast.png', 'JumboBreakfast', 80.43, 9.74);
INSERT INTO `affordable_packages` VALUES (2, '../res/McDonald_packages/DeluxeBreakfast.png', 'DeluxeBreakfast', 99.99, 9.03);
INSERT INTO `affordable_packages` VALUES (3, '../res/McDonald_packages/HotcakesDeluxeBreakfast.png', 'HotcakesDeluxeBreakfast', 87.59, 9.39);
INSERT INTO `affordable_packages` VALUES (4, '../res/McDonald_packages/Filet-O-Fish™.png', 'Filet-O-Fish™', 82.76, 9.01);
INSERT INTO `affordable_packages` VALUES (5, '../res/McDonald_packages/HamN\'CheeseBurger.png', 'HamN\'CheeseBurger', 99.07, 8.22);
INSERT INTO `affordable_packages` VALUES (6, '../res/McDonald_packages/SausageMcMuffin®withEgg.png', 'SausageMcMuffin®withEgg', 93.02, 8.76);
INSERT INTO `affordable_packages` VALUES (7, '../res/McDonald_packages/SausageMcMuffin®.png', 'SausageMcMuffin®', 94.4, 9.95);
INSERT INTO `affordable_packages` VALUES (8, '../res/McDonald_packages/GrilledChickenTwistyPasta.png', 'GrilledChickenTwistyPasta', 92.4, 9.14);
INSERT INTO `affordable_packages` VALUES (9, '../res/McDonald_packages/SausageN’EggTwistyPasta.png', 'SausageN’EggTwistyPasta', 84.85, 9.06);
INSERT INTO `affordable_packages` VALUES (10, '../res/McDonald_packages/HamN\'EggTwistyPasta.png', 'HamN\'EggTwistyPasta', 84.03, 9.82);
INSERT INTO `affordable_packages` VALUES (11, '../res/McDonald_packages/MorningValuePicks-SausageMcMuffin®withEgg.png', 'MorningValuePicks-SausageMcMuffin®withEgg', 88.14, 8.83);
INSERT INTO `affordable_packages` VALUES (12, '../res/McDonald_packages/MorningValuePicks-ScrambledEggsBurger.png', 'MorningValuePicks-ScrambledEggsBurger', 89.58, 9.52);
INSERT INTO `affordable_packages` VALUES (13, '../res/McDonald_packages/MorningValuePicks-HamN’CheeseBurger.png', 'MorningValuePicks-HamN’CheeseBurger', 85.41, 8.84);
INSERT INTO `affordable_packages` VALUES (14, '../res/McDonald_packages/MorningValuePicks-Egg&CheeseBurger.png', 'MorningValuePicks-Egg&CheeseBurger', 84.06, 9.11);
INSERT INTO `affordable_packages` VALUES (15, '../res/McDonald_packages/MorningValuePicks–Filet-O-Fish™.png', 'MorningValuePicks–Filet-O-Fish™', 94.88, 9.81);
INSERT INTO `affordable_packages` VALUES (16, '../res/McDonald_packages/开心乐园餐®-上午11时前.png', '开心乐园餐®-上午11时前', 92.4, 9.89);
INSERT INTO `affordable_packages` VALUES (17, '../res/McDonald_packages/开心乐园餐®-上午11时后.jpg', '开心乐园餐®-上午11时后', 84.56, 8.23);
INSERT INTO `affordable_packages` VALUES (18, '../res/McDonald_packages/珍宝套餐.png', '珍宝套餐', 90.5, 8.33);
INSERT INTO `affordable_packages` VALUES (19, '../res/McDonald_packages/精选早晨套餐.png', '精选早晨套餐', 95.18, 9.28);
INSERT INTO `affordable_packages` VALUES (20, '../res/McDonald_packages/热香饼精选套餐.png', '热香饼精选套餐', 85.21, 8.52);
INSERT INTO `affordable_packages` VALUES (21, '../res/McDonald_packages/板烧鸡腿.png', '板烧鸡腿', 96.69, 9.66);
INSERT INTO `affordable_packages` VALUES (22, '../res/McDonald_packages/猪柳蛋扭扭粉.png', '猪柳蛋扭扭粉', 94.41, 9.21);
INSERT INTO `affordable_packages` VALUES (23, '../res/McDonald_packages/火腿扒蛋.png', '火腿扒蛋', 83.25, 9.89);
INSERT INTO `affordable_packages` VALUES (24, '../res/McDonald_packages/凯撒沙律.png', '凯撒沙律', 89.84, 9.06);
INSERT INTO `affordable_packages` VALUES (25, '../res/McDonald_packages/新吞拿凯撒沙律.png', '新吞拿凯撒沙律', 85.23, 8.58);

-- ----------------------------
-- Table structure for coupon
-- ----------------------------
DROP TABLE IF EXISTS `coupon`;
CREATE TABLE `coupon`  (
  `coupon_id` int(11) NOT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `merchant_id` int(11) NULL DEFAULT NULL,
  `coupon_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `discount_amount` decimal(10, 2) NULL DEFAULT NULL,
  `expiration_date` date NULL DEFAULT NULL,
  PRIMARY KEY (`coupon_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `merchant_id`(`merchant_id`) USING BTREE,
  CONSTRAINT `coupon_ibfk_2` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`merchant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

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
  `delivery_id` int(11) NOT NULL,
  `order_id` int(11) NULL DEFAULT NULL,
  `delivery_address` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `delivery_person_id` int(11) NULL DEFAULT NULL,
  `delivery_status` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`delivery_id`) USING BTREE,
  INDEX `order_id`(`order_id`) USING BTREE,
  INDEX `delivery_person_id`(`delivery_person_id`) USING BTREE,
  CONSTRAINT `delivery_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `ordertable` (`order_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `delivery_ibfk_2` FOREIGN KEY (`delivery_person_id`) REFERENCES `deliveryperson` (`delivery_person_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of delivery
-- ----------------------------
INSERT INTO `delivery` VALUES (1, 1, '配送地址1', 1, '已派送', NULL);
INSERT INTO `delivery` VALUES (2, 2, '配送地址2', 2, '配送中', NULL);

-- ----------------------------
-- Table structure for deliveryperson
-- ----------------------------
DROP TABLE IF EXISTS `deliveryperson`;
CREATE TABLE `deliveryperson`  (
  `delivery_person_id` int(11) NOT NULL,
  `delivery_person_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `contact_number` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`delivery_person_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

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
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`category_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of dishcategory
-- ----------------------------
INSERT INTO `dishcategory` VALUES (1, '热菜');
INSERT INTO `dishcategory` VALUES (2, '凉菜');
INSERT INTO `dishcategory` VALUES (3, '汉堡');
INSERT INTO `dishcategory` VALUES (4, '披萨');
INSERT INTO `dishcategory` VALUES (5, '小食');
INSERT INTO `dishcategory` VALUES (6, '甜品');
INSERT INTO `dishcategory` VALUES (7, '饮品');
INSERT INTO `dishcategory` VALUES (8, '早餐');
INSERT INTO `dishcategory` VALUES (9, '500大卡套餐');
INSERT INTO `dishcategory` VALUES (10, '开心乐园餐');
INSERT INTO `dishcategory` VALUES (11, '普通套餐');

-- ----------------------------
-- Table structure for latest_offers
-- ----------------------------
DROP TABLE IF EXISTS `latest_offers`;
CREATE TABLE `latest_offers`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img_path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `simplified_title` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `simplified_details` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `price` decimal(10, 2) NULL DEFAULT 0.00,
  `discount` decimal(10, 2) NULL DEFAULT 0.00,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 37 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of latest_offers
-- ----------------------------
INSERT INTO `latest_offers` VALUES (19, '../res/McDonald_offers/$27醒晨超值选配热Latte(细)(星期一至五适用，公众假期除外)[可重用].jpg', '$27醒晨超值选配热Latte(细)(星期一至五适用，公众假期除外)[可重用]', '\n                        -指定醒晨超值选:鱼柳饱/猪柳蛋汉堡/炒双蛋饱配McCafé热即磨鲜奶咖啡(细)\r\n-可选: McCafé热即磨鲜奶咖啡(细) / +$3 McCafé热即磨鲜奶咖啡(大) / +$7 McCafé冻即磨鲜奶咖啡\r\n-优惠于星期一至五(公众假期除外)早上6时至早上11时适用\r\n                    ', 27.04, 7.77);
INSERT INTO `latest_offers` VALUES (20, '../res/McDonald_offers/指定早晨套餐减$3.jpg', '指定早晨套餐减$3', '\n                        -此优惠可于选购指定超值早晨套餐(原价$32起)时作$3优惠使用\r\n-可转配或加钱升级其他饮品。升级请参考饮品价目表\r\n-优惠于早上4时至早上11时适用                    ', 11.24, 8.54);
INSERT INTO `latest_offers` VALUES (21, '../res/McDonald_offers/$28韩式甜辣麦炸鸡(2件)配饮品[可重用].jpg', '$28韩式甜辣麦炸鸡(2件)配饮品[可重用]', '\n                        -韩式甜辣麦炸鸡(2件)配饮品(参考价$53.5起)\r\n-可转配或加钱升级其他饮品。升级请参考饮品价目表\r\n-优惠于早上11时至午夜12时适用                    ', 18.08, 9.38);
INSERT INTO `latest_offers` VALUES (22, '../res/McDonald_offers/韩式甜辣麦炸鸡套餐$37(参考价$49.5起)[可重用].jpg', '韩式甜辣麦炸鸡套餐$37(参考价$49.5起)[可重用]', '\n                        +$6升级加大套餐\r\n+$9升级大大啖套餐\r\n-可转配或加钱升级其他饮品。升级请参考饮品价目表\r\n-优惠于早上11时至午夜12时适用\r\n                    ', 49.70, 8.27);
INSERT INTO `latest_offers` VALUES (23, '../res/McDonald_offers/$40蜜糖BBQ麦炸鸡(2件)及饮品配一款小食[可重用].jpg', '$40蜜糖BBQ麦炸鸡(2件)及饮品配一款小食[可重用]', '\n                        -蜜糖BBQ麦炸鸡(2件)及饮品配一款小食(参考价$49.5起)\r\n-可选:中薯条 / 粒粒粟米杯(中) / 苹果批\r\n-可转配或加钱升级其他饮品。升级请参考饮品价目表\r\n-优惠于早上11时至午夜12时适用\r\n                    ', 37.24, 9.23);
INSERT INTO `latest_offers` VALUES (24, '../res/McDonald_offers/$37原味麦炸鸡(2件)及饮品配一款小食[可重用].jpg', '$37原味麦炸鸡(2件)及饮品配一款小食[可重用]', '\n                        -原味麦炸鸡(2件)及饮品配一款小食(参考价$47.5起)\r\n-可选:中薯条 / 粒粒粟米杯(中) / 苹果批\r\n-可转配或加钱升级其他饮品。升级请参考饮品价目表\r\n-优惠于早上11时至午夜12时适用                    ', 30.11, 8.31);
INSERT INTO `latest_offers` VALUES (25, '../res/McDonald_offers/$88起麦炸鸡分享桶(6件)[可重用].jpg', '$88起麦炸鸡分享桶(6件)[可重用]', '\n                        $88(6件原味麦炸鸡)(原价$100起)\r\n$93(6件蜜糖BBQ麦炸鸡或6件韩式甜辣麦炸鸡)(原价$108起)\r\n$93(2件原味麦炸鸡+2件蜜糖BBQ麦炸鸡+2件韩式甜辣麦炸鸡)(原价$108起)\r\n$93(3件原味麦炸鸡+3件蜜糖BBQ麦炸鸡或3件韩式甜辣麦炸鸡)(原价$108起)\r\n-优惠于早上11时至午夜12时适用\r\n                    ', 31.82, 9.88);
INSERT INTO `latest_offers` VALUES (26, '../res/McDonald_offers/[晚上6时起]选购超值套餐送一款小食[可重用].jpg', '[晚上6时起]选购超值套餐送一款小食[可重用]', '\n                        -可选 : OREO麦旋风(1杯)(原价$15.5起)/ 苹果批(原价$9.5起)/麦乐鸡(4件)(参考价$12起)\r\n-优惠不适用于脆爆鸡腿饱套餐、麦炸鸡系列套餐、麦麦食超值套餐包括(麦乐鸡(6件)、猪柳蛋汉堡套餐)及本应用程式最新推介版面内的套餐\r\n-优惠于晚上6时至午夜12时适用                    ', 11.79, 8.45);
INSERT INTO `latest_offers` VALUES (27, '../res/McDonald_offers/McCafé燕麦朱古力及姜饼燕麦咖啡减$3[可重用].jpg', 'McCafé燕麦朱古力及姜饼燕麦咖啡减$3[可重用]', '\n                        -优惠于早上6时至午夜12时适用                    ', 56.47, 8.63);
INSERT INTO `latest_offers` VALUES (28, '../res/McDonald_offers/McCafé奶酱意式饱Combo(原价$49.5起)[全日供应].jpg', 'McCafé奶酱意式饱Combo(原价$49.5起)[全日供应]', '\n                        -优惠于早上6时至午夜12时适用                    ', 39.97, 7.81);
INSERT INTO `latest_offers` VALUES (29, '../res/McDonald_offers/McCafé松饼系列Combo(原价$51.5起)[全日供应].jpg', 'McCafé松饼系列Combo(原价$51.5起)[全日供应]', '\n                        -可选 : 蓝莓松饼/ 朱古力松饼\r\n-优惠于早上6时至午夜12时适用                    ', 23.44, 9.15);
INSERT INTO `latest_offers` VALUES (30, '../res/McDonald_offers/McCafé意式饱系列Combo(原价$61.5起)[全日供应].jpg', 'McCafé意式饱系列Combo(原价$61.5起)[全日供应]', '\n                        -可选 : 火腿蛋沙律意式饱/ 菠萝鸡肉意式饱/ 新吞拿意式饱/ 小龙虾蛋沙律意式饱\r\n-优惠于早上6时至午夜12时适用                    ', 40.28, 9.31);
INSERT INTO `latest_offers` VALUES (31, '../res/McDonald_offers/McCafé热香饼系列Combo(原价$56.5起)[早上11时后供应].jpg', 'McCafé热香饼系列Combo(原价$56.5起)[早上11时后供应]', '\n                        -可选 : 阿华田脆脆热香饼/ OREO脆脆热香饼/ 士多啤梨酱热香饼\r\n-优惠于早上11时至午夜12时适用                    ', 24.09, 9.09);
INSERT INTO `latest_offers` VALUES (32, '../res/McDonald_offers/McCafé蛋糕系列Combo(原价$64起)[全日供应].jpg', 'McCafé蛋糕系列Combo(原价$64起)[全日供应]', '\n                        -可选 : 纽约芝士蛋糕/ 蓝莓芝士蛋糕/ 紫薯慕斯蛋糕\r\n-优惠于早上6时至午夜12时适用                    ', 42.60, 7.53);
INSERT INTO `latest_offers` VALUES (33, '../res/McDonald_offers/【麦麦送专享】$72起韩式甜辣麦炸鸡一人餐(悭$22.5).jpg', '【麦麦送专享】$72起韩式甜辣麦炸鸡一人餐(悭$22.5)', '\n                        套餐包括 : 韩式甜辣麦炸鸡(2件) + 阿华田批或4件麦乐鸡配中薯条(1份)及中汽水(1杯)\r\n-可转配其他饮品。请参考饮品价目表\r\n-优惠于早上11时至午夜12时适用                    ', 33.72, 9.36);
INSERT INTO `latest_offers` VALUES (34, '../res/McDonald_offers/【麦麦送专享】买满$120即送麦乐鸡(9件).jpg', '【麦麦送专享】买满$120即送麦乐鸡(9件)', '\n                        -麦乐鸡(9件)(原价$30起)\r\n-麦麦送订单满HK$120并使用此优惠券，即可免费送麦乐鸡(9件)。HK$120只计算订购食物及饮品之费用\r\n-优惠早上11时至午夜12时适用\r\n                    ', 33.82, 8.24);
INSERT INTO `latest_offers` VALUES (35, '../res/McDonald_offers/【麦麦送专享】买满$150即送麦炸鸡(2件,只限鸡槌).jpg', '【麦麦送专享】买满$150即送麦炸鸡(2件,只限鸡槌)', '\n                        -原味麦炸鸡(2件)(原价$41.5起)、蜜糖BBQ麦炸鸡(2件)(原价$43.5起) \r\n-麦麦送订单满HK$150 并使用此优惠券，即可免费送麦炸鸡 (2件, 只限鸡槌)。HK$150只计算订购食物及饮品之费用\r\n-可选原味麦炸鸡或蜜糖 BBQ 麦炸鸡\r\n-优惠早上11时至午夜12时适用\r\n                    ', 10.92, 9.13);
INSERT INTO `latest_offers` VALUES (36, '../res/McDonald_offers/【麦麦送专享】买满$300即送麦炸鸡(6件).jpg', '【麦麦送专享】买满$300即送麦炸鸡(6件)', '\n                        -原味麦炸鸡(6件)(原价 $113.5起)，蜜糖BBQ味麦炸鸡(6件)(原价$119.5起)\r\n-麦麦送订单满HK$300并使用此优惠券，即可免费送麦炸鸡(6件)。HK$300只计算订购食物及饮品之费用\r\n-可选原味或蜜糖BBQ味\r\n-优惠于早上11时至午夜12时适用\r\n                    ', 46.14, 7.92);

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `menu_id` int(11) NOT NULL,
  `menu_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `category_id` int(11) NULL DEFAULT NULL,
  `price` double NULL DEFAULT NULL,
  `cover_path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `discount` double NULL DEFAULT NULL,
  PRIMARY KEY (`menu_id`) USING BTREE,
  INDEX `menu_ibfk_1`(`category_id`) USING BTREE,
  CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `dishcategory` (`category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, '菜单1', 1, 69.86, NULL, 9.4);
INSERT INTO `menu` VALUES (2, '菜单2', 2, 85.57, NULL, 9.4);
INSERT INTO `menu` VALUES (3, '巨无霸', 3, 28.25, '../res/McDonald/汉堡/巨无霸.png', 8.7);
INSERT INTO `menu` VALUES (4, '汉堡包', 3, 54.57, '../res/McDonald/汉堡/汉堡包.png', 8.3);
INSERT INTO `menu` VALUES (5, '麦辣鸡腿汉堡', 3, 88.08, '../res/McDonald/汉堡/麦辣鸡腿汉堡.png', 8.5);
INSERT INTO `menu` VALUES (6, '原味板烧鸡腿堡', 3, 86.69, '../res/McDonald/汉堡/原味板烧鸡腿堡.png', 7.5);
INSERT INTO `menu` VALUES (7, '麦香鸡', 3, 69.2, '../res/McDonald/汉堡/麦香鸡.png', 8.2);
INSERT INTO `menu` VALUES (8, '麦香鱼', 3, 75.94, '../res/McDonald/汉堡/麦香鱼.png', 8.2);
INSERT INTO `menu` VALUES (9, '吉士汉堡包', 3, 72.11, '../res/McDonald/汉堡/吉士汉堡包.png', 9.7);
INSERT INTO `menu` VALUES (10, '双层吉士汉堡', 3, 32.72, '../res/McDonald/汉堡/双层吉士汉堡.png', 8);
INSERT INTO `menu` VALUES (11, '不素之霸双层牛堡', 3, 27.26, '../res/McDonald/汉堡/不素之霸双层牛堡.png', 9.6);
INSERT INTO `menu` VALUES (12, '双层深海鳕鱼堡', 3, 28.15, '../res/McDonald/汉堡/双层深海鳕鱼堡.png', 8.2);
INSERT INTO `menu` VALUES (13, '安格斯MAX厚牛培根堡', 3, 48.99, '../res/McDonald/汉堡/安格斯MAX厚牛培根堡.png', 8.1);
INSERT INTO `menu` VALUES (14, '安格斯MAX厚牛芝士堡', 3, 60.47, '../res/McDonald/汉堡/安格斯MAX厚牛芝士堡.png', 8.9);
INSERT INTO `menu` VALUES (15, '双层安格斯MAX厚牛培根堡', 3, 55.4, '../res/McDonald/汉堡/双层安格斯MAX厚牛培根堡.png', 7.2);
INSERT INTO `menu` VALUES (16, '双层安格斯MAX厚牛芝士堡', 3, 85.6, '../res/McDonald/汉堡/双层安格斯MAX厚牛芝士堡.png', 8.2);
INSERT INTO `menu` VALUES (17, '培根蔬萃双层牛堡', 3, 71.81, '../res/McDonald/汉堡/培根蔬萃双层牛堡.png', 9.3);
INSERT INTO `menu` VALUES (18, '可口可乐', 7, 92.22, '../res/McDonald/饮品/可口可乐.png', 9);
INSERT INTO `menu` VALUES (19, '零度可口可乐', 7, 55.66, '../res/McDonald/饮品/零度可口可乐.png', 7.2);
INSERT INTO `menu` VALUES (20, '阳光柠檬红茶', 7, 81.66, '../res/McDonald/饮品/阳光柠檬红茶.png', 8);
INSERT INTO `menu` VALUES (21, '雪碧', 7, 51.31, '../res/McDonald/饮品/雪碧.png', 8.4);
INSERT INTO `menu` VALUES (22, '原味珍珠奶茶', 7, 91.57, '../res/McDonald/饮品/原味珍珠奶茶.png', 8);
INSERT INTO `menu` VALUES (23, '美汁源阳光橙', 7, 23.93, '../res/McDonald/饮品/美汁源阳光橙.png', 7.7);
INSERT INTO `menu` VALUES (24, '美汁源100%苹果汁', 7, 14.93, '../res/McDonald/饮品/美汁源100%苹果汁.png', 7.7);
INSERT INTO `menu` VALUES (25, '优品豆浆', 7, 82.87, '../res/McDonald/饮品/优品豆浆.png', 8.2);
INSERT INTO `menu` VALUES (26, '纯牛奶（UHT)', 7, 89.58, '../res/McDonald/饮品/纯牛奶（UHT).png', 7.8);
INSERT INTO `menu` VALUES (27, '热朱古力', 7, 99.26, '../res/McDonald/饮品/热朱古力.png', 7.6);
INSERT INTO `menu` VALUES (28, '锡兰红茶', 7, 37.56, '../res/McDonald/饮品/锡兰红茶.png', 7.4);
INSERT INTO `menu` VALUES (29, '鲜煮咖啡', 7, 60.03, '../res/McDonald/饮品/鲜煮咖啡.png', 7.2);
INSERT INTO `menu` VALUES (30, '冰露包装饮用水', 7, 87.45, '../res/McDonald/饮品/冰露包装饮用水.png', 9.9);
INSERT INTO `menu` VALUES (31, '薯条', 5, 67.19, '../res/McDonald/小食/薯条.png', 9);
INSERT INTO `menu` VALUES (32, '麦乐鸡 (5块)', 5, 63.58, '../res/McDonald/小食/麦乐鸡 (5块).png', 8.2);
INSERT INTO `menu` VALUES (33, '玉米杯', 5, 16.35, '../res/McDonald/小食/玉米杯.png', 7);
INSERT INTO `menu` VALUES (34, '麦辣鸡翅', 5, 61.02, '../res/McDonald/小食/麦辣鸡翅.png', 9.6);
INSERT INTO `menu` VALUES (35, '那么大鸡排', 5, 66.03, '../res/McDonald/小食/那么大鸡排.png', 7.8);
INSERT INTO `menu` VALUES (36, '苹果片', 5, 47.08, '../res/McDonald/小食/苹果片.png', 9.3);
INSERT INTO `menu` VALUES (37, '麦麦脆汁鸡（琵琶腿）', 5, 27.33, '../res/McDonald/小食/麦麦脆汁鸡（琵琶腿）.png', 7.2);
INSERT INTO `menu` VALUES (38, '麦麦脆汁鸡（鸡胸）', 5, 75.39, '../res/McDonald/小食/麦麦脆汁鸡（鸡胸）.png', 7);
INSERT INTO `menu` VALUES (39, '三拼小食盒', 5, 14.97, '../res/McDonald/小食/三拼小食盒.png', 9.5);
INSERT INTO `menu` VALUES (40, '人气堡堡桶', 5, 18.67, '../res/McDonald/小食/人气堡堡桶.png', 7.3);
INSERT INTO `menu` VALUES (41, '炸鸡天团桶', 5, 38.45, '../res/McDonald/小食/炸鸡天团桶.png', 7.1);
INSERT INTO `menu` VALUES (42, '麦麦炸鸡桶', 5, 36.24, '../res/McDonald/小食/麦麦炸鸡桶.png', 9.8);
INSERT INTO `menu` VALUES (43, '麦麦汉堡桶', 5, 55.85, '../res/McDonald/小食/麦麦汉堡桶.png', 8.4);
INSERT INTO `menu` VALUES (44, '四拼小食桶', 5, 70.52, '../res/McDonald/小食/四拼小食桶.png', 8.7);
INSERT INTO `menu` VALUES (45, '圆筒冰淇淋', 6, 85.07, '../res/McDonald/甜品/圆筒冰淇淋.png', 8.5);
INSERT INTO `menu` VALUES (46, '朱古力新地', 6, 23.8, '../res/McDonald/甜品/朱古力新地.png', 9.3);
INSERT INTO `menu` VALUES (47, '草莓新地', 6, 33.75, '../res/McDonald/甜品/草莓新地.png', 7.9);
INSERT INTO `menu` VALUES (48, '麦旋风™奥利奥原味', 6, 87.39, '../res/McDonald/甜品/麦旋风™奥利奥原味.png', 7.7);
INSERT INTO `menu` VALUES (49, '麦旋风™奥利奥草莓口味', 6, 55.68, '../res/McDonald/甜品/麦旋风™奥利奥草莓口味.png', 8);
INSERT INTO `menu` VALUES (50, '香芋派', 6, 96.24, '../res/McDonald/甜品/香芋派.png', 9.6);
INSERT INTO `menu` VALUES (51, '菠萝派', 6, 34.14, '../res/McDonald/甜品/菠萝派.png', 8.2);
INSERT INTO `menu` VALUES (52, '猪柳麦满分', 8, 51.97, '../res/McDonald/早餐/猪柳麦满分.png', 8.3);
INSERT INTO `menu` VALUES (53, '猪柳蛋麦满分', 8, 57.44, '../res/McDonald/早餐/猪柳蛋麦满分.png', 9.8);
INSERT INTO `menu` VALUES (54, '双层猪柳蛋麦满分', 8, 31.3, '../res/McDonald/早餐/双层猪柳蛋麦满分.png', 8.3);
INSERT INTO `menu` VALUES (55, '吉士蛋麦满分', 8, 64.17, '../res/McDonald/早餐/吉士蛋麦满分.png', 7.9);
INSERT INTO `menu` VALUES (56, '火腿扒麦满分', 8, 36.96, '../res/McDonald/早餐/火腿扒麦满分.png', 7.8);
INSERT INTO `menu` VALUES (57, '双层火腿扒麦满分', 8, 72.27, '../res/McDonald/早餐/双层火腿扒麦满分.png', 8);
INSERT INTO `menu` VALUES (58, '大脆鸡扒麦满分', 8, 60.46, '../res/McDonald/早餐/大脆鸡扒麦满分.png', 9.7);
INSERT INTO `menu` VALUES (59, '原味板烧鸡腿麦满分', 8, 75.51, '../res/McDonald/早餐/原味板烧鸡腿麦满分.png', 8.6);
INSERT INTO `menu` VALUES (60, '双层原味板烧鸡腿麦满分', 8, 96.17, '../res/McDonald/早餐/双层原味板烧鸡腿麦满分.png', 9.9);
INSERT INTO `menu` VALUES (61, '原味板烧鸡腿炒双蛋堡', 8, 64.33, '../res/McDonald/早餐/原味板烧鸡腿炒双蛋堡.png', 7.6);
INSERT INTO `menu` VALUES (62, '猪柳炒双蛋堡', 8, 23.14, '../res/McDonald/早餐/猪柳炒双蛋堡.png', 7.3);
INSERT INTO `menu` VALUES (63, '吉士炒双蛋堡', 8, 92.71, '../res/McDonald/早餐/吉士炒双蛋堡.png', 9.8);
INSERT INTO `menu` VALUES (64, '德式图林根香肠炒双蛋堡', 8, 24.13, '../res/McDonald/早餐/德式图林根香肠炒双蛋堡.png', 8);
INSERT INTO `menu` VALUES (65, '火腿扒早安营养卷', 8, 12.53, '../res/McDonald/早餐/火腿扒早安营养卷.png', 9.8);
INSERT INTO `menu` VALUES (66, '图林根香肠早安营养卷', 8, 70.26, '../res/McDonald/早餐/图林根香肠早安营养卷.png', 8.9);
INSERT INTO `menu` VALUES (67, '皮蛋鸡肉粥', 8, 33.71, '../res/McDonald/早餐/皮蛋鸡肉粥.png', 8);
INSERT INTO `menu` VALUES (68, '雪菜脆笋鸡肉粥', 8, 37.77, '../res/McDonald/早餐/雪菜脆笋鸡肉粥.png', 9.4);
INSERT INTO `menu` VALUES (69, '脆薯饼', 8, 77.71, '../res/McDonald/早餐/脆薯饼.png', 9.9);
INSERT INTO `menu` VALUES (70, '脆香油条', 8, 85.25, '../res/McDonald/早餐/脆香油条.png', 8.5);
INSERT INTO `menu` VALUES (71, '德式图林根香肠', 8, 93.1, '../res/McDonald/早餐/德式图林根香肠.png', 8.6);
INSERT INTO `menu` VALUES (72, '优品豆浆', 8, 19.77, '../res/McDonald/早餐/优品豆浆.png', 7.4);
INSERT INTO `menu` VALUES (78, '儿童鱼排堡', 10, 18.93, '../res/McDonald/开心乐园餐/儿童鱼排堡.png', 7.2);
INSERT INTO `menu` VALUES (79, '汉堡包', 10, 97.09, '../res/McDonald/开心乐园餐/汉堡包.png', 8.3);
INSERT INTO `menu` VALUES (80, '麦乐鸡（4块）', 10, 58.68, '../res/McDonald/开心乐园餐/麦乐鸡（4块）.png', 9.7);
INSERT INTO `menu` VALUES (81, '薯条（迷你）', 10, 82.12, '../res/McDonald/开心乐园餐/薯条（迷你）.png', 7.6);
INSERT INTO `menu` VALUES (82, '玉米杯 (小)', 10, 44.57, '../res/McDonald/开心乐园餐/玉米杯 (小).png', 8.1);
INSERT INTO `menu` VALUES (83, '苹果片', 10, 56.49, '../res/McDonald/开心乐园餐/苹果片.png', 7.6);
INSERT INTO `menu` VALUES (84, '纯牛奶 (UHT)', 10, 48.73, '../res/McDonald/开心乐园餐/纯牛奶 (UHT).png', 9.8);
INSERT INTO `menu` VALUES (85, '美汁源100%苹果汁 (小)', 10, 64.18, '../res/McDonald/开心乐园餐/美汁源100%苹果汁 (小).png', 7.1);
INSERT INTO `menu` VALUES (86, '冰露包装饮用水', 10, 74.69, '../res/McDonald/开心乐园餐/冰露包装饮用水.png', 7.9);

-- ----------------------------
-- Table structure for merchant
-- ----------------------------
DROP TABLE IF EXISTS `merchant`;
CREATE TABLE `merchant`  (
  `merchant_id` int(11) NOT NULL,
  `merchant_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `merchant_address` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `merchant_contact` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `restaurant_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`merchant_id`) USING BTREE,
  INDEX `restaurant_id`(`restaurant_id`) USING BTREE,
  CONSTRAINT `merchant_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of merchant
-- ----------------------------
INSERT INTO `merchant` VALUES (1, '商家A', '商家地址A', '111-222-3333', 1);
INSERT INTO `merchant` VALUES (2, '商家B', '商家地址B', '444-555-6666', 2);

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `restaurant_id` int(11) NULL DEFAULT NULL,
  `order_time` datetime NULL DEFAULT NULL,
  `order_status` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `order_amount` decimal(10, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `restaurant_id`(`restaurant_id`) USING BTREE,
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (1, 1, 1, '2024-01-02 18:18:23', 'Pending', 50.00);
INSERT INTO `orders` VALUES (2, 1, 1, '2024-01-02 18:18:38', 'Pending', 50.00);
INSERT INTO `orders` VALUES (3, 1, 1, '2024-01-02 22:22:57', '已完成', 556.68);
INSERT INTO `orders` VALUES (4, 3, 1, '2024-01-02 22:31:17', '已完成', 28.25);
INSERT INTO `orders` VALUES (5, 4, 1, '2024-01-03 13:10:20', '已完成', 594.84);
INSERT INTO `orders` VALUES (6, 4, 1, '2024-01-03 13:23:37', '已完成', 28.25);
INSERT INTO `orders` VALUES (7, 4, 1, '2024-01-03 13:32:45', '已完成', 86.69);
INSERT INTO `orders` VALUES (8, 4, 1, '2024-01-03 13:49:29', '已完成', 270.40);
INSERT INTO `orders` VALUES (9, 4, 1, '2024-01-03 13:51:42', '已完成', 1039.57);
INSERT INTO `orders` VALUES (10, 4, 1, '2024-01-04 11:00:40', '已完成', 0.00);
INSERT INTO `orders` VALUES (11, 4, 1, '2024-01-04 11:01:04', '已完成', 28.25);
INSERT INTO `orders` VALUES (12, 4, 1, '2024-01-04 11:04:55', '已完成', 32.72);
INSERT INTO `orders` VALUES (13, 4, 1, '2024-01-04 11:15:13', '已完成', 28.25);
INSERT INTO `orders` VALUES (14, 4, 1, '2024-01-04 11:21:43', '已完成', 464.32);
INSERT INTO `orders` VALUES (15, 4, 1, '2024-01-04 13:29:57', '已完成', 359.34);
INSERT INTO `orders` VALUES (16, 4, 1, '2024-01-04 13:30:55', '已完成', 359.34);
INSERT INTO `orders` VALUES (17, 4, 1, '2024-01-04 13:31:13', '已完成', 359.34);
INSERT INTO `orders` VALUES (18, 4, 1, '2024-01-04 13:31:47', '已完成', 459.33);
INSERT INTO `orders` VALUES (19, 4, 1, '2024-01-04 14:10:46', '已完成', 28.25);
INSERT INTO `orders` VALUES (20, 4, 1, '2024-01-04 14:11:16', '已完成', 27.04);
INSERT INTO `orders` VALUES (21, 4, 1, '2024-01-04 14:12:07', '已完成', 55.29);
INSERT INTO `orders` VALUES (22, 4, 1, '2024-01-04 14:19:50', '已完成', 2898.88);
INSERT INTO `orders` VALUES (23, 4, 1, '2024-01-04 14:32:17', '已完成', 348.66);
INSERT INTO `orders` VALUES (24, 4, 1, '2024-01-04 14:33:55', '已完成', 537.84);
INSERT INTO `orders` VALUES (25, 4, 1, '2024-01-04 14:35:43', '已完成', 2165.75);
INSERT INTO `orders` VALUES (26, 4, 1, '2024-01-04 15:36:00', '已完成', 99.99);
INSERT INTO `orders` VALUES (27, 4, 1, '2024-01-04 17:13:11', '已完成', 86.69);
INSERT INTO `orders` VALUES (28, 4, 1, '2024-01-04 17:18:14', '已完成', 0.00);
INSERT INTO `orders` VALUES (29, 4, 1, '2024-01-04 18:13:08', '已完成', 927.07);
INSERT INTO `orders` VALUES (30, 4, 1, '2024-01-04 19:00:33', '已完成', 386.05);
INSERT INTO `orders` VALUES (31, 4, 1, '2024-01-08 16:23:10', '已完成', 343.52);
INSERT INTO `orders` VALUES (32, 4, 1, '2024-01-08 16:27:16', '已完成', 2503.81);
INSERT INTO `orders` VALUES (33, 4, 1, '2024-02-29 18:55:26', '已完成', 203.84);
INSERT INTO `orders` VALUES (34, 4, 1, '2024-05-13 12:48:03', '已完成', 55.85);
INSERT INTO `orders` VALUES (35, 4, 1, '2024-05-18 14:26:21', '已完成', 257.64);
INSERT INTO `orders` VALUES (36, 4, 1, '2024-06-04 20:05:43', '已完成', 330.75);
INSERT INTO `orders` VALUES (37, 4, 1, '2024-06-06 21:25:37', '已完成', 903.94);

-- ----------------------------
-- Table structure for ordertable
-- ----------------------------
DROP TABLE IF EXISTS `ordertable`;
CREATE TABLE `ordertable`  (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `merchant_id` int(11) NULL DEFAULT NULL,
  `dish_id` int(11) NULL DEFAULT NULL,
  `order_time` datetime NULL DEFAULT NULL,
  `order_status` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `discount_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `discount_amount` decimal(10, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `merchant_id`(`merchant_id`) USING BTREE,
  INDEX `dish_id`(`dish_id`) USING BTREE,
  CONSTRAINT `ordertable_ibfk_2` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`merchant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ordertable_ibfk_3` FOREIGN KEY (`dish_id`) REFERENCES `menu` (`menu_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ordertable
-- ----------------------------
INSERT INTO `ordertable` VALUES (1, 1, 1, 1, '2024-01-03 18:45:00', '已下单', NULL, NULL);
INSERT INTO `ordertable` VALUES (2, 2, 2, 2, '2024-01-04 20:15:00', '已完成', NULL, NULL);

-- ----------------------------
-- Table structure for restaurant
-- ----------------------------
DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE `restaurant`  (
  `restaurant_id` int(11) NOT NULL,
  `restaurant_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `restaurant_address` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `contact_number` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of restaurant
-- ----------------------------
INSERT INTO `restaurant` VALUES (1, '餐厅A', '地址A', '123-456-7890');
INSERT INTO `restaurant` VALUES (2, '餐厅B', '地址B', '987-654-3210');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_realname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_gender` tinyint(1) NULL DEFAULT NULL,
  `user_birthday` date NULL DEFAULT NULL,
  `user_email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone_number` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '用户1', '密码1', '张三', 1, '1990-01-01', 'user1@example.com', '111-222-3333');
INSERT INTO `user` VALUES (2, '用户2', '密码2', '李四', 0, '1985-05-15', 'user2@example.com', '444-555-6666');
INSERT INTO `user` VALUES (3, 'new_user', '', 'New User', 1, '1990-01-01', 'new_user@example.com', '123-456-7890');
INSERT INTO `user` VALUES (4, 'existing_username', 'azure', 'azure', 1, '1990-01-01', 'azure@example.com', '1234567890');

-- ----------------------------
-- Table structure for usermerchantlogin
-- ----------------------------
DROP TABLE IF EXISTS `usermerchantlogin`;
CREATE TABLE `usermerchantlogin`  (
  `record_id` int(11) NOT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `merchant_id` int(11) NULL DEFAULT NULL,
  `login_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`record_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `merchant_id`(`merchant_id`) USING BTREE,
  CONSTRAINT `usermerchantlogin_ibfk_2` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`merchant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

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
  `review_id` int(11) NOT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `merchant_id` int(11) NULL DEFAULT NULL,
  `rating` int(11) NULL DEFAULT NULL,
  `review_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `review_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`review_id`) USING BTREE,
  INDEX `merchant_id`(`merchant_id`) USING BTREE,
  INDEX `userreview_ibfk_1`(`user_id`) USING BTREE,
  CONSTRAINT `userreview_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `userreview_ibfk_2` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`merchant_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of userreview
-- ----------------------------
INSERT INTO `userreview` VALUES (1, 1, 1, 4, '好吃！', '2024-01-05 10:00:00');
INSERT INTO `userreview` VALUES (2, 2, 2, 5, '非常好！', '2024-01-06 11:30:00');

SET FOREIGN_KEY_CHECKS = 1;
