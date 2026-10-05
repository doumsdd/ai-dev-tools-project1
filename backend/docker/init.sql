-- Script d'initialisation PostgreSQL pour guestBTP
-- Ce script est exécuté automatiquement au premier démarrage du conteneur

-- Extension pour les types numériques précis (optionnel)
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- Pour recherche fuzzy future

-- Création d'index pour optimiser les requêtes courantes
-- Ces index seront créés après les tables par SQLAlchemy

-- Note: Les tables sont créées automatiquement par SQLAlchemy
-- via Base.metadata.create_all() au démarrage de l'application

-- Pour ajouter des données de test, décommentez les lignes ci-dessous:
/*
INSERT INTO clients (name, email, phone, address, siret, client_type, archived)
VALUES
    ('Entreprise Durand', 'contact@durand-btp.fr', '+33 1 23 45 67 89', '12 rue du Chantier, 75012 Paris', '12345678901234', 'entreprise', false),
    ('Mairie de Lyon', 'contact@mairie-lyon.fr', '+33 4 72 10 30 30', '1 place de la Comédie, 69001 Lyon', '21690123100011', 'maitre_ouvrage', false);
*/
