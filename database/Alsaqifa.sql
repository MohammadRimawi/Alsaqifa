-- phpMyAdmin SQL Dump
-- version 4.9.7deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 07, 2021 at 01:22 PM
-- Server version: 8.0.23-3ubuntu1
-- PHP Version: 7.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Alsaqifa`
--

-- --------------------------------------------------------

--
-- Table structure for table `authentication`
--

CREATE TABLE `authentication` (
  `user_id` int NOT NULL,
  `username` tinytext NOT NULL,
  `password` tinytext NOT NULL,
  `email` tinytext NOT NULL,
  `role` tinytext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `playlists`
--

CREATE TABLE `playlists` (
  `playlist_id` int NOT NULL,
  `name` tinytext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `playlists`
--

INSERT INTO `playlists` (`playlist_id`, `name`) VALUES
(1, 'Test playlist');

-- --------------------------------------------------------

--
-- Table structure for table `playlists_tracks`
--

CREATE TABLE `playlists_tracks` (
  `playlist_id` int NOT NULL,
  `track_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `playlists_tracks`
--

INSERT INTO `playlists_tracks` (`playlist_id`, `track_id`) VALUES
(1, 1),
(1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `title` text NOT NULL,
  `description` text NOT NULL,
  `text` text NOT NULL,
  `image_url` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `posted_by` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_id`, `user_id`, `title`, `description`, `text`, `image_url`, `posted_by`) VALUES
(1, 1, 'تيست 1', 'هذا تيست مخصص للتستتة،وليس تيست عادي وحسب ', 'هذا تيست مخصص للتستتة،وليس تيست عادي وحسب هذا تيست مخصص للتستتة،وليس تيست عادي وحسب هذا تيست مخصص للتستتة،وليس تيست عادي وحسب ر', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1),
(2, 1, 'تيست 2', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1),
(3, 1, 'تيست 3', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1),
(4, 1, 'تيست 4', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1),
(5, 1, 'تيست 5', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1),
(6, 1, 'تيست 6', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1),
(7, 1, 'تيست 7', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1),
(8, 1, 'تيست 8', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1),
(9, 1, 'تيست 9', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1),
(10, 1, 'تيست 10', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.هذا تيست ثاني مخصص للتستتة، وليس مجرد تيست وحسب.', 'assets/images/ERTaFf3XYAEYQqs.jpg', 1);

-- --------------------------------------------------------

--
-- Table structure for table `posts_comments`
--

CREATE TABLE `posts_comments` (
  `comment_id` int NOT NULL,
  `post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `comment` text NOT NULL,
  `reply_to` int DEFAULT NULL,
  `likes` int NOT NULL,
  `dislikes` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `posts_tags`
--

CREATE TABLE `posts_tags` (
  `post_id` int NOT NULL,
  `tag_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `posts_tags`
--

INSERT INTO `posts_tags` (`post_id`, `tag_id`) VALUES
(1, 3),
(3, 3),
(5, 3),
(7, 3),
(9, 3),
(2, 2),
(4, 2),
(6, 2),
(8, 2),
(10, 2),
(2, 1),
(4, 1),
(6, 1),
(1, 1),
(9, 1),
(10, 1);

-- --------------------------------------------------------

--
-- Table structure for table `slider_widget`
--

CREATE TABLE `slider_widget` (
  `slider_id` int NOT NULL,
  `widget_id` int NOT NULL,
  `number_of_cards` int NOT NULL,
  `order_by` tinytext NOT NULL,
  `tag_id` int DEFAULT NULL,
  `preview_type` tinytext NOT NULL,
  `shuffle` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `slider_widget`
--

INSERT INTO `slider_widget` (`slider_id`, `widget_id`, `number_of_cards`, `order_by`, `tag_id`, `preview_type`, `shuffle`) VALUES
(1, 1, 5, 'latest', 1, 'descriptive', 1);

-- --------------------------------------------------------

--
-- Table structure for table `tags`
--

CREATE TABLE `tags` (
  `tag_id` int NOT NULL,
  `tag_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tags`
--

INSERT INTO `tags` (`tag_id`, `tag_name`) VALUES
(1, 'تيست تاج'),
(2, 'زوجي'),
(3, 'فردي');

-- --------------------------------------------------------

--
-- Table structure for table `tracks`
--

CREATE TABLE `tracks` (
  `track_id` int NOT NULL,
  `name` tinytext NOT NULL,
  `image_url` text NOT NULL,
  `track_url` text NOT NULL,
  `duration` tinytext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tracks`
--

INSERT INTO `tracks` (`track_id`, `name`, `image_url`, `track_url`, `duration`) VALUES
(1, 'التراك الاول', '/assets/images/ERTaFf3XYAEYQqs.jpg', '/audio/deep-thoughts-full_G10GtE4O_NWM', '1:39'),
(2, 'التراك الثاني', '/assets/images/ERTaFf3XYAEYQqs.jpg', 'audio/audioblocks-escaping-forever_BwdtBTFiS_NWM', '2:41');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `name` tinytext NOT NULL,
  `title` tinytext,
  `image_url` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `title`, `image_url`) VALUES
(1, 'Mohammad Rimawi', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users_tags`
--

CREATE TABLE `users_tags` (
  `user_id` int NOT NULL,
  `tag_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `widgets`
--

CREATE TABLE `widgets` (
  `widget_id` int NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` tinytext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `widgets`
--

INSERT INTO `widgets` (`widget_id`, `name`, `type`) VALUES
(1, 'تيست 1', 'slider');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authentication`
--
ALTER TABLE `authentication`
  ADD KEY `authentication_user_id_fk` (`user_id`);

--
-- Indexes for table `playlists`
--
ALTER TABLE `playlists`
  ADD PRIMARY KEY (`playlist_id`);

--
-- Indexes for table `playlists_tracks`
--
ALTER TABLE `playlists_tracks`
  ADD KEY `playlists_tracks_playlist_id_fk` (`playlist_id`),
  ADD KEY `playlists_tracks_track_id_fk` (`track_id`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_id`),
  ADD KEY `posts_user_id_fk` (`user_id`),
  ADD KEY `posted_by_user_id_fk` (`posted_by`);

--
-- Indexes for table `posts_comments`
--
ALTER TABLE `posts_comments`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `comment_post_id_fk` (`post_id`),
  ADD KEY `comment_user_id_fk` (`user_id`),
  ADD KEY `comment_reply_to_fk` (`reply_to`);

--
-- Indexes for table `posts_tags`
--
ALTER TABLE `posts_tags`
  ADD KEY `post_tag_post_id_fk` (`post_id`),
  ADD KEY `post_tag_tag_id_fk` (`tag_id`);

--
-- Indexes for table `slider_widget`
--
ALTER TABLE `slider_widget`
  ADD PRIMARY KEY (`slider_id`),
  ADD KEY `slider_widget_id_fk` (`widget_id`),
  ADD KEY `slider_tag_id_fk` (`tag_id`);

--
-- Indexes for table `tags`
--
ALTER TABLE `tags`
  ADD PRIMARY KEY (`tag_id`);

--
-- Indexes for table `tracks`
--
ALTER TABLE `tracks`
  ADD PRIMARY KEY (`track_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `users_tags`
--
ALTER TABLE `users_tags`
  ADD KEY `user_tag_user_id_fk` (`user_id`),
  ADD KEY `user_tag_tag_id_fk` (`tag_id`);

--
-- Indexes for table `widgets`
--
ALTER TABLE `widgets`
  ADD PRIMARY KEY (`widget_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `playlists`
--
ALTER TABLE `playlists`
  MODIFY `playlist_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `post_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `posts_comments`
--
ALTER TABLE `posts_comments`
  MODIFY `comment_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `slider_widget`
--
ALTER TABLE `slider_widget`
  MODIFY `slider_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tags`
--
ALTER TABLE `tags`
  MODIFY `tag_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tracks`
--
ALTER TABLE `tracks`
  MODIFY `track_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `widgets`
--
ALTER TABLE `widgets`
  MODIFY `widget_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `authentication`
--
ALTER TABLE `authentication`
  ADD CONSTRAINT `authentication_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `playlists_tracks`
--
ALTER TABLE `playlists_tracks`
  ADD CONSTRAINT `playlists_tracks_playlist_id_fk` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`playlist_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `playlists_tracks_track_id_fk` FOREIGN KEY (`track_id`) REFERENCES `tracks` (`track_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posted_by_user_id_fk` FOREIGN KEY (`posted_by`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `posts_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `posts_comments`
--
ALTER TABLE `posts_comments`
  ADD CONSTRAINT `comment_post_id_fk` FOREIGN KEY (`post_id`) REFERENCES `posts` (`post_id`),
  ADD CONSTRAINT `comment_reply_to_fk` FOREIGN KEY (`reply_to`) REFERENCES `posts_comments` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `comment_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `posts_tags`
--
ALTER TABLE `posts_tags`
  ADD CONSTRAINT `post_tag_post_id_fk` FOREIGN KEY (`post_id`) REFERENCES `posts` (`post_id`),
  ADD CONSTRAINT `post_tag_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`);

--
-- Constraints for table `slider_widget`
--
ALTER TABLE `slider_widget`
  ADD CONSTRAINT `slider_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `slider_widget_id_fk` FOREIGN KEY (`widget_id`) REFERENCES `widgets` (`widget_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `users_tags`
--
ALTER TABLE `users_tags`
  ADD CONSTRAINT `user_tag_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`),
  ADD CONSTRAINT `user_tag_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
