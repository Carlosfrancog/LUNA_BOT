import discord
from discord.ext import commands
import os
from key import *
import random
from time import sleep


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
async def Acargo(ctx, member: discord.Member, role_name: str):
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
async def Rcargo(ctx, member: discord.Member, role_name: str):
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
async def Ncargo(ctx, cargo_nome: str):
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
async def Mcargo(ctx, cargo_nome: str):
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
async def Dcargo(ctx, cargo_nome: str):
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
async def clear(ctx,amount=100):
    if ctx.author.guild_permissions.ban_members:
        await ctx.channel.purge(limit=amount)
        await ctx.send('**As 100 últimas mensagens foram apagadas com sucesso!**',delete_after=5)
    else:
        falta = 'Você não tem permissão para usar esse comando!'
        embed = discord.Embed(title=f"{falta}")
        await ctx.send(embed=embed)


@client.command()
async def oi(ctx):
        RespOi = ['Olá!', 'Como vai?', 'Prazer, sou a Luna', 'Oi', 'Não me atrapalha peste!']
        list = RespOi
        Escolha = random.choice(list)
        print(Escolha)
    
        await ctx.send(f'**{Escolha}**')





client.run(TOKEN)            