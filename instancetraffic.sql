

-- ----------------------------
-- Table structure for instancetraffic
-- ----------------------------
DROP TABLE IF EXISTS `instancetraffic`;
CREATE TABLE `instancetraffic`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `linode_id` int(11) NOT NULL,
  `linode_label` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `dataCenter` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `publicIp` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `instanceType` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `traffic_usage` decimal(20, 0) NULL DEFAULT NULL,
  `traffic_usage_GB` decimal(20, 4) NULL DEFAULT NULL,
  `traffic_quota` decimal(20, 0) NULL DEFAULT NULL,
  `traffic_billable` decimal(20, 0) NULL DEFAULT NULL,
  `traffic_billable_GB` decimal(20, 4) NULL DEFAULT NULL,
  `createDt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updateDt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_instancetraffic_linode_label`(`linode_label`) USING BTREE,
  INDEX `ix_instancetraffic_dataCenter`(`dataCenter`) USING BTREE,
  INDEX `ix_instancetraffic_linode_id`(`linode_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3854840 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
