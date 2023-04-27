import discord
from discord.ext import commands
import os
from key import *
import random
from time import sleep
import json

wallet_file = os.path.join(os.path.dirname(__file__), 'wallet.json')

TOKEN = seu_token()
msg_id = None
msg_user = None


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True
intents.bans = True
intents.emojis = True
intents.integrations = True
intents.webhooks = True
intents.invites = True
intents.voice_states = True
intents.presences = True
intents.reactions = True
intents.typing = True


client = commands.Bot(command_prefix="+", case_insensitive = True, intents=intents)
#client.remove_command('help')


@client.event #bot on
async def on_ready():
    try:
        print('O BOT {0.user} etsá funcionado'.format(client))
        if client.is_ready():
            await client.change_presence(activity=discord.Game(name='RPG e pronta para ajudar!😘'))
    except Exception as e:
        print(f'Erro ao iniciar o BOT: {e}')

    
@client.command()
async def devtest(ctx):
    """
    Comando de testes na versão de desenvolvimento
    """
    
    dev_role = discord.utils.get(ctx.guild.roles, name="dev")
    if dev_role in ctx.author.roles:
        if ctx.message.content == "+devtest":  
            embed = discord.Embed(
                title='Número Aleatório',
                description=f'***Olá, {ctx.author}. Vejo que possui permissão para usar o comando "devtest"***',
                color=discord.Color.green()
            )
            embed_mensage = await ctx.channel.send(embed=embed)
            await embed_mensage.add_reaction('🟢')  
    else:
        embed = discord.Embed(
            title='PERMISSÃO NEGADA❕',
            description=f'***{ctx.author} NÃO TEM PERMISSÃO PARA USAR ESSE COMANDO 😡***',
            color=discord.Color.red()
        )
        embed_mensage = await ctx.channel.send(embed=embed)
        await embed_mensage.add_reaction('❌')


@client.command() #dar cargo
async def addrule(ctx, member: discord.Member, role_name: str):
    """
    Dá um cargo para um membro
    """
    
    # Verifica se o autor tem permissões de gerenciar cargos
    if ctx.author.guild_permissions.manage_roles:
        # Obtém o objeto de cargo com base no nome fornecido
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            # Adiciona o cargo ao membro
            await member.add_roles(role)
            # Cria um embed para a mensagem de confirmação
            embed = discord.Embed(
                title='Cargo Adicionado',
                description=f'O cargo **{role_name}** foi adicionado ao membro {member.name}.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            # Cria um embed para a mensagem de erro
            embed = discord.Embed(
                title='Erro',
                description='Não foi possível encontrar o cargo especificado.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    else:
        # Cria um embed para a mensagem de erro
        embed = discord.Embed(
            title='Erro',
            description='Você não possui permissões para gerenciar cargos.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        

@client.command() #retirar cargo
async def removerule(ctx, member: discord.Member, role_name: str):
    # Verifica se o autor tem permissões de gerenciar cargos
    if ctx.author.guild_permissions.manage_roles:
        # Obtém o objeto de cargo com base no nome fornecido
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            # Verifica se o membro possui o cargo antes de remover
            if role in member.roles:
                # Remove o cargo do membro
                await member.remove_roles(role)
                # Cria um embed para a mensagem de confirmação
                embed = discord.Embed(
                    title='Cargo Removido',
                    description=f'O cargo **{role_name}** foi removido do membro {member.name}.',
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                # Cria um embed para a mensagem de erro
                embed = discord.Embed(
                    title='Erro',
                    description=f'O membro {member.name} não possui o cargo especificado.',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            # Cria um embed para a mensagem de erro
            embed = discord.Embed(
                title='Erro',
                description='Não foi possível encontrar o cargo especificado.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    else:
        # Cria um embed para a mensagem de erro
        embed = discord.Embed(
            title='Erro',
            description='Você não possui permissões para gerenciar cargos.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@client.command() #criar cargo
@commands.has_permissions(manage_roles=True)
async def createrule(ctx, cargo_nome: str):
    guild = ctx.guild

    # Verificar se o cargo já existe
    role = discord.utils.get(guild.roles, name=cargo_nome)
    if role:
        embed = discord.Embed(
            title='Erro',
            description='Esse cargo já existe.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    # Criar o cargo com cor verde
    try:
        cor_verde = discord.Colour.green()
        role = await guild.create_role(name=cargo_nome, colour=cor_verde)
        embed = discord.Embed(
            title='Cargo Criado',
            description=f'O cargo {role.name} foi criado com sucesso.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(
            title='Erro',
            description='Não foi possível criar o cargo. Verifique as permissões do bot.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(
            title='Erro',
            description='Ocorreu um erro ao criar o cargo.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

        
@client.command() #criar cargo MOD
async def modrule(ctx, cargo_nome: str):
    # Verifica se o autor tem permissões de administrador
    if ctx.author.guild_permissions.administrator:
        # Cria o cargo com as permissões de moderadores
        permissions = discord.Permissions()
        permissions.ban_members = True
        permissions.kick_members = True
        permissions.manage_roles = True
        permissions.manage_nicknames = True
        permissions.move_members = True
        permissions.mute_members = True
        permissions.deafen_members = True
        role = await ctx.guild.create_role(name=cargo_nome, permissions=permissions)
        # Define a cor do cargo como verde
        await role.edit(colour=discord.Color.green())
        # Cria um embed para a mensagem de confirmação
        embed = discord.Embed(
            title='Cargo Criado',
            description=f'O cargo **{cargo_nome}** foi criado com permissões de moderadores.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        # Cria um embed para a mensagem de erro
        embed = discord.Embed(
            title='Erro',
            description='Você não possui permissões de administrador para criar um cargo com permissões de moderadores.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)       
        
        
@client.command() #deletar cargo
async def deleterule(ctx, cargo_nome: str):
    # Verifica se o autor tem permissões de administrador
    if ctx.author.guild_permissions.administrator:
        # Busca o cargo pelo nome
        role = discord.utils.get(ctx.guild.roles, name=cargo_nome)
        if role:
            # Remove o cargo
            await role.delete()
            # Cria um embed para a mensagem de confirmação
            embed = discord.Embed(
                title='Cargo Excluído',
                description=f'O cargo **{cargo_nome}** foi excluído.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            # Cria um embed para a mensagem de erro
            embed = discord.Embed(
                title='Erro',
                description=f'O cargo **{cargo_nome}** não foi encontrado.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    else:
        # Cria um embed para a mensagem de erro
        embed = discord.Embed(
            title='Erro',
            description='Você não possui permissões de administrador para excluir um cargo.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

        
@client.command(aliases=['c']) #limpar chat
async def clear(ctx, amount=100):
    if not ctx.guild:
        await ctx.send("Este comando só pode ser usado em um servidor.")
        return
    member = ctx.author
    if isinstance(member, discord.User):
        member = ctx.guild.get_member(member.id)
    if member.guild_permissions.ban_members:
        await ctx.channel.purge(limit=amount)
        await ctx.send('**As 100 últimas mensagens foram apagadas com sucesso!**', delete_after=5)
    else:
        falta = 'Você não tem permissão para usar esse comando!'
        embed = discord.Embed(title=f"{falta}")
        await ctx.send(embed=embed)



def new_wallet(member_id, member_name):
    if not os.path.exists(wallet_file):
        with open(wallet_file, 'w') as f:
            json.dump({}, f)
    
    with open(wallet_file, 'r+') as f:
        wallets = json.load(f)
        if member_id in wallets:
            return 'Você já possui uma carteira registrada!'
        else:
            wallets[member_id] = {"user_name": member_name, "balance": 0, "transactions": []}
            f.seek(0)
            json.dump(wallets, f, indent=4)
            f.truncate()
            return 'Sua carteira foi criada com sucesso!'


async def show_balance(ctx, member_id):
    with open(wallet_file, 'r') as f:
        wallets = json.load(f)

    if member_id not in wallets:
        return 'Você ainda não possui carteira registrada. Use o comando +newwallet para criar uma.'
    else:
        balance = wallets[member_id]['balance']
        return f'Seu saldo atual é de {balance} coins 🪙'



@client.command()
async def newwallet(ctx):
    member_id = str(ctx.author.id)
    member_name = ctx.author.name
    message = new_wallet(member_id, member_name)
    await ctx.send(message)

    
@client.command()
async def wallet(ctx):
    member_id = str(ctx.author.id)
    message = await show_balance(ctx, member_id)
    if 'Erro' in message:
        await ctx.author.send(embed=discord.Embed(title='Erro', description=message))
    else:
        embed = discord.Embed(title='Saldo', description=message)
        msg = await ctx.author.send(embed=embed)
        await msg.add_reaction('🤑')

@client.command()
async def addcoins(ctx, amount: int):
    member_id = str(ctx.author.id)
    with open(wallet_file, 'r') as f:
        json.dump({}, f)
        wallets = json.load(f)

    if member_id not in wallets:
        await ctx.send('Você ainda não possui carteira registrada. Use o comando +newwallet para criar uma.')
        return

    wallets[member_id]['balance'] += amount

    with open(wallet_file, 'w') as f:
        json.dump(wallets, f)

    await ctx.send(f'Foram adicionadas {amount} coins à sua carteira.')


@client.command()
async def removecoins(ctx, amount: int):
    member_id = str(ctx.author.id)
    with open(wallet_file, 'r') as f:
        json.dump({}, f)
        wallets = json.load(f)

    if member_id not in wallets:
        await ctx.send('Você ainda não possui carteira registrada. Use o comando +newwallet para criar uma.')
        return

    if amount >= wallets[member_id]['balance'] :
        wallets[member_id]['balance'] -= wallets[member_id]['balance'] 
    else:
        wallets[member_id]['balance'] -= amount

    with open(wallet_file, 'w') as f:
        json.dump(wallets, f)

    if wallets[member_id]['balance'] == 0:
        await ctx.send(f'***Você tem 0 coins!***')
    else:
        await ctx.send(f'Foram retiradas {amount} coins à sua carteira.')
        
        
        
@client.command()
async def pix(ctx, member: discord.Member, amount: int):
    member_id = str(member.id)
    author_id = str(ctx.author.id)
    with open(wallet_file, 'r') as f:
        wallets = json.load(f)

    if member_id not in wallets:
        await ctx.send('Você ainda não possui carteira registrada. Use o comando +newwallet para criar uma.')
        return

    balance_author = wallets[author_id]['balance']
    
    if amount <= balance_author:
        wallets[author_id]['balance'] -= amount
        wallets[author_id]["transactions"].append({'type': 'ExitMoney', 'amount': amount, 'payer': member_id})
        
        wallets[member_id]['balance'] += amount
        wallets[member_id]["transactions"].append({'type': 'JoinMoney', 'amount': amount, 'receiver': author_id})
        
        with open(wallet_file, 'w') as f:
            json.dump(wallets, f, indent=4)  
            
        embed = discord.Embed(title='PIX REALIZADO! 🟢', description=f'***{ctx.author} fez um pix para {member} no valor de {amount}***', color=discord.Color.orange())
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('⬆️')
        await msg.add_reaction('💸')
        await msg.add_reaction('⬇️')
    else: 
        await ctx.send(f'***Saldo insuficiente!\n{ctx.author} tem {balance_author}***')







@client.command()
async def oi(ctx):
        RespOi = ['Olá!', 'Como vai?', 'Prazer, sou a Luna', 'Oi', 'Não me atrapalha peste!']
        list = RespOi
        Escolha = random.choice(list)
        print(Escolha)
    
        await ctx.send(f'**{Escolha}**')



client.run(TOKEN) 