import sys
import numpy as np
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QTabWidget, QComboBox, QTextEdit, 
                           QLineEdit, QGridLayout, QGroupBox, QMessageBox, QRadioButton,
                           QButtonGroup, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CryptographieApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Application de Cryptographie")
        self.setGeometry(100, 100, 900, 700)
        
        # Création des tables et carrés
        self.carre_polybique = self.generer_carre_polybique()
        self.table_vigenere = self.generer_table_vigenere()
        
        # Création de l'interface
        self.init_ui()
    
    def init_ui(self):
        # Widget central et layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # En-tête
        header_label = QLabel("Application de Cryptographie")
        header_label.setAlignment(Qt.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        main_layout.addWidget(header_label)
        
        # Onglets pour les différentes méthodes
        self.tabs = QTabWidget()
        
        # Onglet pour la cryptographie classique
        classic_tab = QTabWidget()
        
        # Onglet pour le chiffrement polybique
        polybique_tab = QWidget()
        self.setup_polybique_tab(polybique_tab)
        classic_tab.addTab(polybique_tab, "Carré Polybique")
        
        # Onglet pour le chiffrement de Vigenère
        vigenere_tab = QWidget()
        self.setup_vigenere_tab(vigenere_tab)
        classic_tab.addTab(vigenere_tab, "Vigenère")
        
        # Ajouter l'onglet de cryptographie classique
        self.tabs.addTab(classic_tab, "Cryptographie Classique")
        
        # Onglet pour la cryptographie moderne (placeholder)
        modern_tab = QWidget()
        self.setup_modern_tab(modern_tab)
        self.tabs.addTab(modern_tab, "Cryptographie Moderne")
        
        main_layout.addWidget(self.tabs)
        
        # Bouton Quitter
        quit_button = QPushButton("Quitter")
        quit_button.clicked.connect(self.close)
        main_layout.addWidget(quit_button)
    
    # --- Configuration des onglets ---
    
    def setup_polybique_tab(self, tab):
        layout = QVBoxLayout(tab)
        
        # Groupe pour afficher le carré polybique
        carre_group = QGroupBox("Carré Polybique")
        carre_layout = QVBoxLayout()
        
        # Tableau pour afficher le carré
        self.polybique_table = QTableWidget(6, 6)
        self.polybique_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.polybique_table.horizontalHeader().setVisible(False)
        self.polybique_table.verticalHeader().setVisible(False)
        
        # Remplir le tableau avec le carré polybique
        for i in range(6):
            self.polybique_table.setColumnWidth(i, 40)
            for j in range(6):
                item = QTableWidgetItem(str(self.carre_polybique[i, j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.polybique_table.setItem(i, j, item)
        
        carre_layout.addWidget(self.polybique_table)
        carre_group.setLayout(carre_layout)
        layout.addWidget(carre_group)
        
        # Groupe pour les opérations
        operations_group = QGroupBox("Opérations")
        operations_layout = QVBoxLayout()
        
        # Boutons radio pour choisir l'opération
        radio_layout = QHBoxLayout()
        self.polybique_radio_group = QButtonGroup()
        
        self.polybique_chiffrer_radio = QRadioButton("Chiffrer")
        self.polybique_chiffrer_radio.setChecked(True)
        self.polybique_dechiffrer_radio = QRadioButton("Déchiffrer")
        
        self.polybique_radio_group.addButton(self.polybique_chiffrer_radio)
        self.polybique_radio_group.addButton(self.polybique_dechiffrer_radio)
        
        radio_layout.addWidget(self.polybique_chiffrer_radio)
        radio_layout.addWidget(self.polybique_dechiffrer_radio)
        operations_layout.addLayout(radio_layout)
        
        # Champ de texte pour l'entrée
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Texte:"))
        self.polybique_input = QTextEdit()
        input_layout.addWidget(self.polybique_input)
        operations_layout.addLayout(input_layout)
        
        # Bouton d'action
        polybique_action_button = QPushButton("Appliquer")
        polybique_action_button.clicked.connect(self.appliquer_polybique)
        operations_layout.addWidget(polybique_action_button)
        
        # Champ de texte pour la sortie
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Résultat:"))
        self.polybique_output = QTextEdit()
        self.polybique_output.setReadOnly(True)
        output_layout.addWidget(self.polybique_output)
        operations_layout.addLayout(output_layout)
        
        operations_group.setLayout(operations_layout)
        layout.addWidget(operations_group)
    
    def setup_vigenere_tab(self, tab):
        layout = QVBoxLayout(tab)
        
        # Groupe pour les opérations
        operations_group = QGroupBox("Opérations")
        operations_layout = QVBoxLayout()
        
        # Boutons radio pour choisir l'opération
        radio_layout = QHBoxLayout()
        self.vigenere_radio_group = QButtonGroup()
        
        self.vigenere_chiffrer_radio = QRadioButton("Chiffrer")
        self.vigenere_chiffrer_radio.setChecked(True)
        self.vigenere_dechiffrer_radio = QRadioButton("Déchiffrer")
        
        self.vigenere_radio_group.addButton(self.vigenere_chiffrer_radio)
        self.vigenere_radio_group.addButton(self.vigenere_dechiffrer_radio)
        
        radio_layout.addWidget(self.vigenere_chiffrer_radio)
        radio_layout.addWidget(self.vigenere_dechiffrer_radio)
        operations_layout.addLayout(radio_layout)
        
        # Champ de texte pour l'entrée
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Texte:"))
        self.vigenere_input = QTextEdit()
        input_layout.addWidget(self.vigenere_input)
        operations_layout.addLayout(input_layout)
        
        # Champ pour la clé
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("Clé:"))
        self.vigenere_key = QLineEdit()
        key_layout.addWidget(self.vigenere_key)
        operations_layout.addLayout(key_layout)
        
        # Case à cocher pour clé aléatoire
        random_key_layout = QHBoxLayout()
        self.vigenere_random_key = QRadioButton("Générer une clé aléatoire")
        self.vigenere_user_key = QRadioButton("Utiliser la clé ci-dessus")
        self.vigenere_user_key.setChecked(True)
        
        key_radio_group = QButtonGroup()
        key_radio_group.addButton(self.vigenere_random_key)
        key_radio_group.addButton(self.vigenere_user_key)
        
        random_key_layout.addWidget(self.vigenere_random_key)
        random_key_layout.addWidget(self.vigenere_user_key)
        operations_layout.addLayout(random_key_layout)
        
        # Bouton d'action
        vigenere_action_button = QPushButton("Appliquer")
        vigenere_action_button.clicked.connect(self.appliquer_vigenere)
        operations_layout.addWidget(vigenere_action_button)
        
        # Champ de texte pour la sortie
        output_layout = QGridLayout()
        output_layout.addWidget(QLabel("Résultat:"), 0, 0)
        self.vigenere_output = QTextEdit()
        self.vigenere_output.setReadOnly(True)
        output_layout.addWidget(self.vigenere_output, 0, 1)
        
        output_layout.addWidget(QLabel("Clé utilisée:"), 1, 0)
        self.vigenere_used_key = QLineEdit()
        self.vigenere_used_key.setReadOnly(True)
        output_layout.addWidget(self.vigenere_used_key, 1, 1)
        
        operations_layout.addLayout(output_layout)
        
        operations_group.setLayout(operations_layout)
        layout.addWidget(operations_group)
        
        # Groupe pour afficher la table de Vigenère
        table_group = QGroupBox("Table de Vigenère")
        table_layout = QVBoxLayout()
        
        # Bouton pour afficher la table
        show_table_button = QPushButton("Afficher/Masquer la Table")
        show_table_button.clicked.connect(self.toggle_vigenere_table)
        table_layout.addWidget(show_table_button)
        
        # Tableau pour afficher la table (initialement caché)
        self.vigenere_table_widget = QTableWidget(26, 26)
        self.vigenere_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.vigenere_table_widget.setVisible(False)
        
        # Remplir les en-têtes
        for i in range(26):
            self.vigenere_table_widget.setHorizontalHeaderItem(i, QTableWidgetItem(chr(65 + i)))
            self.vigenere_table_widget.setVerticalHeaderItem(i, QTableWidgetItem(chr(65 + i)))
        
        # Remplir le tableau avec la table de Vigenère
        for i in range(26):
            for j in range(26):
                item = QTableWidgetItem(self.table_vigenere[i, j])
                item.setTextAlignment(Qt.AlignCenter)
                self.vigenere_table_widget.setItem(i, j, item)
        
        self.vigenere_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.vigenere_table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        table_layout.addWidget(self.vigenere_table_widget)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
    
    def setup_modern_tab(self, tab):
        layout = QVBoxLayout(tab)
        
        # Message d'information
        info_label = QLabel("Cette section sera implémentée ultérieurement.\n\n"
                          "Elle pourrait inclure des algorithmes comme :\n"
                          "- RSA\n"
                          "- AES\n"
                          "- Diffie-Hellman\n"
                          "- Courbes elliptiques")
        info_label.setAlignment(Qt.AlignCenter)
        
        font = QFont()
        font.setPointSize(12)
        info_label.setFont(font)
        
        layout.addWidget(info_label)
    
    # --- Méthodes pour le carré polybique ---
    
    def generer_carre_polybique(self):
        """Génère un carré polybique 5x5 avec I/J fusionnés"""
        alphabet = []
        for c in range(ord("A"), ord("Z") + 1):  # Parcourt les codes ASCII de A à Z
            if chr(c) != "J":  # Exclut la lettre "J"
                alphabet.append(chr(c))
        
        # Fusionner "I" et "J" ensemble
        alphabet.insert(alphabet.index("I"), "I/J")
        alphabet.remove("I")  # Supprimer le "I" en double

        carre = np.empty((6, 6), dtype=object)  # Matrice 6x6 pour inclure indices

        # Ajouter les indices (1-5) dans la première ligne et colonne
        carre[0, 0] = " "
        for i in range(1, 6):
            carre[0, i] = str(i)
            carre[i, 0] = str(i)

        # Remplir la matrice avec l'alphabet corrigé
        index = 0
        for i in range(1, 6):
            for j in range(1, 6):
                carre[i, j] = alphabet[index]
                index += 1

        return carre
    
    def chiffrer_polybique(self, texte):
        """Chiffre un texte avec le carré polybique"""
        texte = self.nettoyer_texte(texte)
        texte_chiffre = []

        # Parcours du texte
        for lettre in texte:
            if lettre == "J":
                lettre = "I/J"  # Fusionner I et J
            
            for i in range(1, 6):
                for j in range(1, 6):
                    if self.carre_polybique[i, j] == lettre:
                        texte_chiffre.append(f"{i}{j}")  # Ajouter coordonnées
                        break

        return " ".join(texte_chiffre)
    
    def dechiffrer_polybique(self, texte_chiffre):
        """Déchiffre un texte chiffré avec le carré polybique"""
        # Supprimer les espaces et regrouper par paires
        coordonnees = texte_chiffre.replace(" ", "")
        texte_clair = []
        
        for i in range(0, len(coordonnees), 2):
            if i+1 < len(coordonnees):  # Vérifier qu'il y a bien 2 chiffres
                ligne = int(coordonnees[i])
                colonne = int(coordonnees[i+1])
                
                # Vérifier que les coordonnées sont valides
                if 1 <= ligne <= 5 and 1 <= colonne <= 5:
                    texte_clair.append(self.carre_polybique[ligne, colonne])
        
        # Remplacer "I/J" par "I" pour simplifier
        texte_clair = [lettre.replace("I/J", "I") for lettre in texte_clair]
        
        return "".join(texte_clair)
    
    def appliquer_polybique(self):
        """Applique le chiffrement ou déchiffrement polybique"""
        texte = self.polybique_input.toPlainText().strip()
        
        if not texte:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte.")
            return
        
        if self.polybique_chiffrer_radio.isChecked():
            resultat = self.chiffrer_polybique(texte)
        else:
            resultat = self.dechiffrer_polybique(texte)
        
        self.polybique_output.setText(resultat)
    
    # --- Méthodes pour Vigenère ---
    
    def generer_table_vigenere(self):
        """Génère la table de Vigenère sous forme de matrice NumPy"""
        alphabet = np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        matrice_vigenere = np.zeros((26, 26), dtype=str)
        
        for i in range(26):
            matrice_vigenere[i] = np.roll(alphabet, -i)
        
        return matrice_vigenere
    
    def toggle_vigenere_table(self):
        """Affiche ou masque la table de Vigenère"""
        current_state = self.vigenere_table_widget.isVisible()
        self.vigenere_table_widget.setVisible(not current_state)
    
    def generer_clef_aleatoire(self, longueur):
        """Génère une clé aléatoire de la longueur spécifiée"""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(alphabet) for _ in range(longueur))
    
    def chiffrer_vigenere(self, texte, clef=None):
        """Chiffre un texte avec le chiffre de Vigenère"""
        table_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        texte = self.nettoyer_texte(texte)
        
        if not texte:
            return "", ""
        
        # Générer une clé aléatoire si aucune n'est fournie
        if clef is None or clef == "":
            clef = self.generer_clef_aleatoire(len(texte))
        else:
            clef = self.nettoyer_texte(clef)
            # Répéter la clé pour qu'elle ait la même longueur que le texte
            clef = (clef * (len(texte) // len(clef) + 1))[:len(texte)]
        
        mot_crypte = []
        
        for i in range(len(texte)):
            indice_texte = table_alpha.index(texte[i])
            indice_clef = table_alpha.index(clef[i])
            indice_crypte = (indice_texte + indice_clef) % 26
            mot_crypte.append(table_alpha[indice_crypte])
        
        return clef, "".join(mot_crypte)
    
    def dechiffrer_vigenere(self, texte_chiffre, clef):
        """Déchiffre un texte chiffré avec le chiffre de Vigenère"""
        table_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        texte_chiffre = self.nettoyer_texte(texte_chiffre)
        clef = self.nettoyer_texte(clef)
        
        if not texte_chiffre or not clef:
            return ""
        
        # Répéter la clé pour qu'elle ait la même longueur que le texte
        clef = (clef * (len(texte_chiffre) // len(clef) + 1))[:len(texte_chiffre)]
        
        mot_clair = []
        
        for i in range(len(texte_chiffre)):
            indice_chiffre = table_alpha.index(texte_chiffre[i])
            indice_clef = table_alpha.index(clef[i])
            indice_clair = (indice_chiffre - indice_clef) % 26
            mot_clair.append(table_alpha[indice_clair])
        
        return "".join(mot_clair)
    
    def appliquer_vigenere(self):
        """Applique le chiffrement ou déchiffrement de Vigenère"""
        texte = self.vigenere_input.toPlainText().strip()
        
        if not texte:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte.")
            return
        
        if self.vigenere_chiffrer_radio.isChecked():
            # Chiffrement
            if self.vigenere_random_key.isChecked():
                # Utiliser une clé aléatoire
                clef, resultat = self.chiffrer_vigenere(texte)
            else:
                # Utiliser la clé fournie
                clef_fournie = self.vigenere_key.text().strip()
                clef, resultat = self.chiffrer_vigenere(texte, clef_fournie)
            
            self.vigenere_output.setText(resultat)
            self.vigenere_used_key.setText(clef)
        
        else:
            # Déchiffrement
            clef = self.vigenere_key.text().strip()
            
            if not clef:
                QMessageBox.warning(self, "Attention", "Une clé est nécessaire pour le déchiffrement.")
                return
            
            resultat = self.dechiffrer_vigenere(texte, clef)
            self.vigenere_output.setText(resultat)
            self.vigenere_used_key.setText(clef)
    
    # --- Méthodes utilitaires ---
    
    def nettoyer_texte(self, texte):
        """Supprime les espaces et convertit en majuscules"""
        return "".join(c for c in texte.upper() if c.isalpha())


# Démarrer l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptographieApp()
    window.show()
    sys.exit(app.exec_())