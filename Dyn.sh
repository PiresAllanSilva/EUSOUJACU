#!/bin/bash
echo "Seus arquivos estão preparados para a dinâmica? (Y)es; (N)o" #Your files are already equilibrated and parametrized? (Y)es; (N)o"
read EQ

case $EQ in #Validação dos passos preparatórios da dinâmica.
"Y")

	;;
"N")
	echo "Por favor, insira o nome do arquivo .pdb" #Please, type  the name of PDB file:"
		read PDB
	echo "Atenção: Lembre-se sempre que este é um script em Bash. Dessa forma, todos os nomes recebidos são considerados Case Sensitive." #Warning: Remember that we are using a Bash script. Then, all typings have to be case sensitive."
	echo "Qual campo de força você deseja usar? (A)mberGS; (C)harmm27; (G)romos96; (O)PLS-AA/L; O(T)her"
		read FF

	case $FF in
		"A")
			FFN="7"
			;;
		"C")
			FFN="8"
			;;
		"G")
			FFN="9"
			;;
		"O")
			FFN="15"
			;;
		"T")
			FFN="CORE DUMP"
			echo "Atenção: Se você deseja usar outro campo de força, faça seu próprio Script, preguiçoso." #Warning: If you want to use any other force field, please write your own script lazy."
			;;
	esac

	echo $FFN | pdb2gmx -f $PDB.pdb -o $PDB\_processed.gro -water spc
	editconf -f $PDB\_processed.gro -o $PDB\_newbox.gro -c -d 0.8 -bt cubic
	genbox -cp $PDB\_newbox.gro -cs spc216.gro -o $PDB\_solv.gro -p topol.top
	SOL= grep "SOL" topol.top | awk '{print $2}'
	read SOL
	N="275"
	echo $ions
	grompp -f ions.mdp -c $PDB\_solv.gro -p topol.top -o ions.tpr
	echo "Qual a carga do sistema?"
		read CARGA
	echo "(P)ositiva ou (N)egativa"	
		read PONE

	case $PONE in
		"P")
			NA=$(bc <<< "($SOL/$N)")
			CL=$(bc <<< "($SOL/$N)+$CARGA") #Calcula quantos íons de NA e CL são necessários para 0.2M de NaCl
			;;
		"N")
			CL=$(bc <<< "($SOL/$N)")
			NA=$(bc <<< "($SOL/$N)+$CARGA") #Calcula quantos íons de NA e CL são necessários para 0.2M de NaCl
			;;
		*)
			echo "Opção inválida!"
			;;
	esac

	echo 13 | genion -s ions.tpr -o $PDB\_solv_ions.gro -p topol.top -pname NA -nname CL -np $NA -nn $CL
	grompp -f minim.mdp -c $PDB\_solv_ions.gro -p topol.top -o em.tpr
	mdrun -deffnm em -v 
	grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr
	mdrun -deffnm nvt -v
	grompp -f npt.mdp -c nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
	mdrun -deffnm npt -v
	grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o full.tpr
	;;
*)
	echo "Are you an idiot? Please, set a possible parameter!"
esac
echo "Deseja iniciar a Dinâmica? (Y)es; (N)o"
	read START
case $START in
	"Y")
		echo "Número de réplicas: "
			read REPLICAS
		for ((a=1; a<=$LIMITE; a++))
		do
			if [$a == "1"] 
			then
				mkdir $a
				cd $a
				cp full.tpr $a
				#nohup mdrun -deffnm full -v
				echo "Dynamics 1"
			else 
				cd ../
				mkdir $a
				cd $a
				echo "Dynamics +1"
				cp ../full.tpr .
				#nohup mdrun -deffnm full -v
			fi
		done
		;;
	"N")
		echo "\"Acabou o programa!\" Choque de cultura"
		;;
esac
