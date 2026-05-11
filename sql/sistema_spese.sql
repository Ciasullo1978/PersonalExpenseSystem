-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Mag 11, 2026 alle 19:08
-- Versione del server: 10.1.38-MariaDB
-- Versione PHP: 5.6.40

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sistema_spese`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `budget`
--

CREATE TABLE `budget` (
  `id_budget` int(11) NOT NULL,
  `mese` varchar(7) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `importo` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `budget`
--

INSERT INTO `budget` (`id_budget`, `mese`, `id_categoria`, `importo`) VALUES
(1, '2026-10', 1, '400.00'),
(2, '2026-10', 2, '100.00'),
(3, '2026-10', 4, '150.00'),
(4, '2026-11', 1, '450.00'),
(5, '2026-11', 2, '100.00');

-- --------------------------------------------------------

--
-- Struttura della tabella `categorie`
--

CREATE TABLE `categorie` (
  `id_categoria` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `categorie`
--

INSERT INTO `categorie` (`id_categoria`, `nome`) VALUES
(3, 'Affitto'),
(1, 'Alimentari'),
(5, 'Salute'),
(4, 'Svago'),
(2, 'Trasporti');

-- --------------------------------------------------------

--
-- Struttura della tabella `spese`
--

CREATE TABLE `spese` (
  `id_spesa` int(11) NOT NULL,
  `data_spesa` date NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `importo` decimal(10,2) NOT NULL,
  `descrizione` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `spese`
--

INSERT INTO `spese` (`id_spesa`, `data_spesa`, `id_categoria`, `importo`, `descrizione`) VALUES
(1, '2026-10-05', 1, '55.20', 'Spesa Esselunga'),
(2, '2026-10-12', 1, '42.00', 'Mercato rionale'),
(3, '2026-10-15', 2, '50.00', 'Ricarica Abbonamento Treno'),
(4, '2026-10-20', 4, '85.00', 'Cena fuori con amici'),
(5, '2026-10-25', 1, '120.00', 'Scorta mensile alimentari'),
(6, '2026-10-28', 4, '70.00', 'Biglietti Cinema e Popcorn'),
(7, '2026-11-02', 1, '60.00', 'Spesa Lidl'),
(8, '2026-11-05', 3, '650.00', 'Affitto mensile'),
(9, '2026-11-10', 5, '45.00', 'Visita Dentista');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `budget`
--
ALTER TABLE `budget`
  ADD PRIMARY KEY (`id_budget`),
  ADD UNIQUE KEY `mese` (`mese`,`id_categoria`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- Indici per le tabelle `categorie`
--
ALTER TABLE `categorie`
  ADD PRIMARY KEY (`id_categoria`),
  ADD UNIQUE KEY `nome` (`nome`);

--
-- Indici per le tabelle `spese`
--
ALTER TABLE `spese`
  ADD PRIMARY KEY (`id_spesa`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `budget`
--
ALTER TABLE `budget`
  MODIFY `id_budget` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT per la tabella `categorie`
--
ALTER TABLE `categorie`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT per la tabella `spese`
--
ALTER TABLE `spese`
  MODIFY `id_spesa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `budget`
--
ALTER TABLE `budget`
  ADD CONSTRAINT `budget_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorie` (`id_categoria`) ON DELETE CASCADE;

--
-- Limiti per la tabella `spese`
--
ALTER TABLE `spese`
  ADD CONSTRAINT `spese_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorie` (`id_categoria`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
