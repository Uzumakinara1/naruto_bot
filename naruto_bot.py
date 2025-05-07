import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import random
import time
from datetime import datetime, timedelta

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token
TOKEN = "8176829483:AAHirUnye1yheY3JT0HumWtaQXvg-M63Qso"

# Clan options
CLANS = {
    "uzumaki": "🍃 Uzumaki Clan - Masters of Sealing Jutsu and immense chakra reserves",
    "uchiha": "⚡ Uchiha Clan - Wielders of the Sharingan with unmatched combat prowess",
    "hyuga": "💧 Hyuga Clan - Specialists in the Byakugan and the Gentle Fist technique",
    "senju": "🔥 Senju Clan - Founders of Konoha, possessing incredible vitality and skill"
}

# User data storage (in production, use a database)
user_data = {}

# Start command
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_message = f"👋 Welcome, {user.first_name}!\n" \
                     "To begin your Shinobi Journey, you must join the official Ninja Academy channels! " \
                     "Strengthen your skills and unlock exclusive missions!\n\n" \
                     "📌 Join now:\n\n" \
                     "🌀 Join 🌟 [https://t.me/+pJy0_D0OrVI5Mjc0]\n" \
                     "⚡ Join ⚡ [https://t.me/+ej4ZYg3IIQozYjU0]\n" \
                     "🔥 Join 🔥 [https://t.me/+Ww1QFdOMtrw4NDI0]\n" \
                     "🎯 Finish 🫡 (Only available after joining all groups)"
    
    update.message.reply_text(welcome_message)
    
    # Simulate training sequence
    time.sleep(3)
    update.message.reply_text("🔥 Starting Training...")
    time.sleep(2)
    update.message.reply_text("💨 Assessing Shinobi Profile...")
    time.sleep(1)
    
    # Final welcome message
    welcome_message2 = f"🔥 Welcome to Naruto Legacy, {user.first_name}! ⚔️💨\n" \
                      "Your Ninja Way starts now! 🌟\n\n" \
                      "🔮 Choose Your Path:\n" \
                      "Join the ranks of the Leaf Village Genin, face legendary Akatsuki, or master powerful Jutsu.\n\n" \
                      "⚔️ Battle for Glory:\n" \
                      "Engage in fierce Shinobi Duels, complete missions, and earn respect among the Ninja ranks.\n\n" \
                      "🏆 Compete and Thrive:\n" \
                      "Challenge rivals, join Tournaments, and train under legendary masters.\n" \
                      "Rise to become the Hokage!\n\n" \
                      f"🔥 Your adventure begins now, {user.first_name}! Start your ninja training and prepare for battle! 🔥\n\n" \
                      "📌 Begin Your Journey:\n" \
                      "🎯 Start Your Ninja Path ✌️ (Command: /create)"
    
    update.message.reply_text(welcome_message2)

# Create command - Start creating ninja profile
def create(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_data[user.id] = {"step": "waiting_for_name"}
    
    update.message.reply_text("🌟 Let's create your Shinobi Profile! 🌟\n\n"
                             "1️⃣ Shinobi Name:\n"
                             "📝 Please enter your ninja name (this will be your identity in the ninja world):")

# Handle text messages (for name input)
def handle_text(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    text = update.message.text
    
    if user.id in user_data:
        if user_data[user.id]["step"] == "waiting_for_name":
            user_data[user.id]["name"] = text
            user_data[user.id]["step"] = "waiting_for_clan"
            
            # Create clan selection buttons
            keyboard = [
                [InlineKeyboardButton("🍃 Uzumaki Clan", callback_data='uzumaki')],
                [InlineKeyboardButton("⚡ Uchiha Clan", callback_data='uchiha')],
                [InlineKeyboardButton("💧 Hyuga Clan", callback_data='hyuga')],
                [InlineKeyboardButton("🔥 Senju Clan", callback_data='senju')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            update.message.reply_text(
                "2️⃣ Clan Selection:\n"
                "🌀 Choose your lineage from the options below:",
                reply_markup=reply_markup
            )
        else:
            update.message.reply_text("Please complete your profile creation first!")
    else:
        update.message.reply_text("Please start with /create to begin your ninja journey!")

# Clan selection callback
def clan_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user
    clan = query.data
    
    if user.id in user_data:
        user_data[user.id]["clan"] = clan
        user_data[user.id]["step"] = "waiting_for_picture"
        
        query.answer()
        query.edit_message_text(
            text=f"✅ Clan selected: {CLANS[clan]}\n\n"
                 "3️⃣ Ninja Profile Picture:\n"
                 "🖼️ You can now upload a profile picture (optional).\n"
                 "If you don't want to upload, type /skip"
        )
    else:
        query.answer("Please start with /create first!", show_alert=True)

# Handle photo upload
def handle_photo(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    if user.id in user_data and user_data[user.id]["step"] == "waiting_for_picture":
        photo = update.message.photo[-1]
        user_data[user.id]["photo"] = photo.file_id
        complete_profile(update, user.id)
    else:
        update.message.reply_text("Please complete your profile creation first!")

# Skip photo upload
def skip_photo(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    if user.id in user_data and user_data[user.id]["step"] == "waiting_for_picture":
        user_data[user.id]["photo"] = None
        complete_profile(update, user.id)
    else:
        update.message.reply_text("Please complete your profile creation first!")

# Complete profile creation
def complete_profile(update: Update, user_id: int) -> None:
    user_data[user_id]["step"] = "completed"
    user_data[user_id]["level"] = 1
    user_data[user_id]["xp"] = 0
    user_data[user_id]["stats"] = {
        "strength": random.randint(5, 10),
        "speed": random.randint(5, 10),
        "chakra": random.randint(5, 10),
        "intelligence": random.randint(5, 10)
    }
    
    clan_icon = {
        "uzumaki": "🍃",
        "uchiha": "⚡",
        "hyuga": "💧",
        "senju": "🔥"
    }.get(user_data[user_id]["clan"], "🌀")
    
    message = f"🎉 Shinobi Profile Complete! 🎉\n\n" \
              f"{clan_icon} {user_data[user_id]['name']} of the {user_data[user_id]['clan'].capitalize()} Clan\n" \
              f"Level: 1 | XP: 0/100\n\n" \
              f"💪 Strength: {user_data[user_id]['stats']['strength']}\n" \
              f"⚡ Speed: {user_data[user_id]['stats']['speed']}\n" \
              f"🌀 Chakra: {user_data[user_id]['stats']['chakra']}\n" \
              f"📘 Intelligence: {user_data[user_id]['stats']['intelligence']}\n\n" \
              f"Your ninja journey begins now! Use /train to improve your skills or /battle to test your might!"
    
    if user_data[user_id]["photo"]:
        update.message.reply_photo(
            photo=user_data[user_id]["photo"],
            caption=message
        )
    else:
        update.message.reply_text(message)

# Story command
def story(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Chapter 1: The Call to Destiny", callback_data='chapter_1')],
        [InlineKeyboardButton("Chapter 2: The Academy Test", callback_data='chapter_2')],
        [InlineKeyboardButton("Continue Your Journey", callback_data='continue')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "📖 Naruto Legacy Story Mode\n\n"
        "Choose a chapter to begin or continue your adventure:",
        reply_markup=reply_markup
    )

# Handle story choices
def handle_story_choice(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    choice = query.data
    
    if choice == 'chapter_1':
        query.answer()
        query.edit_message_text(
            text="🏯 Chapter 1: The Call to Destiny\n\n"
                 "The Hidden Leaf Village trembles...\n"
                 "A mysterious figure moves through the shadows. Do you wish to investigate?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Continue", callback_data='chapter_1_continue')],
                [InlineKeyboardButton("❌ Exit Story Mode", callback_data='exit_story')]
            ])
        )
    elif choice == 'chapter_1_continue':
        query.answer()
        query.edit_message_text(
            text="🔥 Explosions shake the Ninja Academy!\n"
                 "You spot an enemy infiltrator launching attacks! What do you do?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚔️ Fight", callback_data='chapter_1_fight')],
                [InlineKeyboardButton("🏃 Evade", callback_data='chapter_1_evade')]
            ])
        )
    elif choice == 'chapter_1_fight':
        query.answer()
        query.edit_message_text(
            text="💀 Battle Begins!\n\n"
                 "You engage the enemy in combat!\n"
                 "Use /battle commands to fight!"
        )
    elif choice == 'chapter_1_evade':
        query.answer()
        query.edit_message_text(
            text="🏃 You successfully evade the enemy!\n\n"
                 "But the threat to the village remains...\n"
                 "Will you report this to the Hokage?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Report to Hokage", callback_data='chapter_1_report')],
                [InlineKeyboardButton("Investigate alone", callback_data='chapter_1_investigate')]
            ])
        )
    elif choice == 'exit_story':
        query.answer()
        query.edit_message_text(text="Story mode exited. Use /story to continue your adventure later!")

# Battle command
def battle(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id not in user_data:
        update.message.reply_text("Please create your ninja profile first with /create!")
        return
    
    # Generate random enemy
    enemies = [
        {"name": "Rogue Ninja", "health": 50, "attack": 8, "speed": 6},
        {"name": "Akatsuki Member", "health": 80, "attack": 12, "speed": 8},
        {"name": "Elite Shinobi", "health": 65, "attack": 10, "speed": 9}
    ]
    enemy = random.choice(enemies)
    
    # Initialize battle data
    user_data[user.id]["battle"] = {
        "enemy": enemy,
        "enemy_health": enemy["health"],
        "user_health": 100,
        "in_battle": True
    }
    
    keyboard = [
        [InlineKeyboardButton("⚔️ Attack", callback_data='battle_attack')],
        [InlineKeyboardButton("🛡️ Defend", callback_data='battle_defend')],
        [InlineKeyboardButton("💊 Use Item", callback_data='battle_item')],
        [InlineKeyboardButton("🏃 Flee", callback_data='battle_flee')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        f"⚔️ Battle against {enemy['name']}!\n\n"
        f"❤️ Your Health: 100\n"
        f"💀 Enemy Health: {enemy['health']}\n\n"
        "Choose your action:",
        reply_markup=reply_markup
    )

# Handle battle actions
def handle_battle_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user
    action = query.data.split('_')[1]
    
    if user.id not in user_data or "battle" not in user_data[user.id]:
        query.answer("No active battle found!", show_alert=True)
        return
    
    battle_data = user_data[user.id]["battle"]
    enemy = battle_data["enemy"]
    
    if action == "attack":
        # User attack
        damage = user_data[user.id]["stats"]["strength"] + random.randint(1, 5)
        battle_data["enemy_health"] -= damage
        
        # Enemy attack
        enemy_damage = max(0, enemy["attack"] - random.randint(0, 3))
        battle_data["user_health"] -= enemy_damage
        
        # Check battle outcome
        if battle_data["enemy_health"] <= 0:
            # User wins
            xp_gain = enemy["health"] // 5
            user_data[user.id]["xp"] += xp_gain
            level_up = check_level_up(user.id)
            
            win_message = f"🎉 Victory! You defeated {enemy['name']}!\n" \
                          f"➕ Gained {xp_gain} XP\n"
            if level_up:
                win_message += f"🌟 Level Up! You are now level {user_data[user.id]['level']}!\n"
            
            query.edit_message_text(
                text=win_message + "\nUse /battle to fight again or /train to improve your skills!"
            )
            del user_data[user.id]["battle"]
        elif battle_data["user_health"] <= 0:
            # User loses
            query.edit_message_text(
                text=f"💀 Defeat! {enemy['name']} was too strong!\n\n"
                     "Use /train to improve your skills and try again!"
            )
            del user_data[user.id]["battle"]
        else:
            # Battle continues
            keyboard = [
                [InlineKeyboardButton("⚔️ Attack", callback_data='battle_attack')],
                [InlineKeyboardButton("🛡️ Defend", callback_data='battle_defend')],
                [InlineKeyboardButton("💊 Use Item", callback_data='battle_item')],
                [InlineKeyboardButton("🏃 Flee", callback_data='battle_flee')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            query.edit_message_text(
                text=f"⚔️ You attacked {enemy['name']} for {damage} damage!\n"
                     f"💀 {enemy['name']} counterattacked for {enemy_damage} damage!\n\n"
                     f"❤️ Your Health: {battle_data['user_health']}\n"
                     f"💀 Enemy Health: {battle_data['enemy_health']}\n\n"
                     "Choose your next action:",
                reply_markup=reply_markup
            )
    
    elif action == "defend":
        # User defends - reduce damage
        enemy_damage = max(0, enemy["attack"] // 2 - random.randint(0, 2))
        battle_data["user_health"] -= enemy_damage
        
        keyboard = [
            [InlineKeyboardButton("⚔️ Attack", callback_data='battle_attack')],
            [InlineKeyboardButton("🛡️ Defend", callback_data='battle_defend')],
            [InlineKeyboardButton("💊 Use Item", callback_data='battle_item')],
            [InlineKeyboardButton("🏃 Flee", callback_data='battle_flee')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            text=f"🛡️ You defended against {enemy['name']}'s attack!\n"
                 f"💀 Only took {enemy_damage} damage!\n\n"
                 f"❤️ Your Health: {battle_data['user_health']}\n"
                 f"💀 Enemy Health: {battle_data['enemy_health']}\n\n"
                 "Choose your next action:",
            reply_markup=reply_markup
        )
    
    elif action == "flee":
        # Try to flee
        if random.random() < 0.7:  # 70% chance to flee
            query.edit_message_text(
                text=f"🏃 You successfully escaped from {enemy['name']}!\n\n"
                     "Use /battle to fight again when you're ready!"
            )
            del user_data[user.id]["battle"]
        else:
            # Failed to flee - take damage
            enemy_damage = enemy["attack"] + random.randint(0, 3)
            battle_data["user_health"] -= enemy_damage
            
            if battle_data["user_health"] <= 0:
                query.edit_message_text(
                    text=f"💀 {enemy['name']} caught you trying to flee and defeated you!\n\n"
                         "Use /train to improve your skills and try again!"
                )
                del user_data[user.id]["battle"]
            else:
                keyboard = [
                    [InlineKeyboardButton("⚔️ Attack", callback_data='battle_attack')],
                    [InlineKeyboardButton("🛡️ Defend", callback_data='battle_defend')],
                    [InlineKeyboardButton("💊 Use Item", callback_data='battle_item')],
                    [InlineKeyboardButton("🏃 Flee", callback_data='battle_flee')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                query.edit_message_text(
                    text=f"❌ {enemy['name']} blocked your escape!\n"
                         f"💀 Took {enemy_damage} damage while trying to flee!\n\n"
                         f"❤️ Your Health: {battle_data['user_health']}\n"
                         f"💀 Enemy Health: {battle_data['enemy_health']}\n\n"
                         "Choose your next action:",
                    reply_markup=reply_markup
                )
    
    elif action == "item":
        # Use item (simplified)
        query.answer("Item feature coming soon! For now, choose another action.", show_alert=True)

# Check if user leveled up
def check_level_up(user_id: int) -> bool:
    xp_needed = user_data[user_id]["level"] * 100
    if user_data[user_id]["xp"] >= xp_needed:
        user_data[user_id]["level"] += 1
        user_data[user_id]["xp"] = 0
        
        # Improve stats on level up
        for stat in user_data[user_id]["stats"]:
            user_data[user_id]["stats"][stat] += random.randint(1, 3)
        
        return True
    return False

# Train command
def train(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id not in user_data:
        update.message.reply_text("Please create your ninja profile first with /create!")
        return
    
    keyboard = [
        [InlineKeyboardButton("🏯 Taijutsu Training (Strength)", callback_data='train_strength')],
        [InlineKeyboardButton("🌀 Chakra Control (Chakra)", callback_data='train_chakra')],
        [InlineKeyboardButton("⚔️ Weapon Mastery (Speed)", callback_data='train_speed')],
        [InlineKeyboardButton("🔥 Sparring Matches (All Stats)", callback_data='train_all')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "🍃 Training Grounds 🍃\n\n"
        "Choose your training method to improve your skills:",
        reply_markup=reply_markup
    )

# Handle training choices
def handle_training(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user
    training_type = query.data.split('_')[1]
    
    if user.id not in user_data:
        query.answer("Please create your ninja profile first with /create!", show_alert=True)
        return
    
    # Simulate training with random improvements
    xp_gain = random.randint(10, 25)
    user_data[user.id]["xp"] += xp_gain
    
    if training_type == "strength":
        stat_gain = random.randint(1, 3)
        user_data[user.id]["stats"]["strength"] += stat_gain
        message = f"💪 You trained hard in Taijutsu!\n" \
                  f"➕ Strength +{stat_gain}\n" \
                  f"➕ Gained {xp_gain} XP"
    elif training_type == "chakra":
        stat_gain = random.randint(1, 3)
        user_data[user.id]["stats"]["chakra"] += stat_gain
        message = f"🌀 You focused on Chakra Control!\n" \
                  f"➕ Chakra +{stat_gain}\n" \
                  f"➕ Gained {xp_gain} XP"
    elif training_type == "speed":
        stat_gain = random.randint(1, 3)
        user_data[user.id]["stats"]["speed"] += stat_gain
        message = f"⚡ You practiced Weapon Mastery!\n" \
                  f"➕ Speed +{stat_gain}\n" \
                  f"➕ Gained {xp_gain} XP"
    elif training_type == "all":
        stat_gain = 1
        for stat in user_data[user.id]["stats"]:
            user_data[user.id]["stats"][stat] += stat_gain
        message = f"🔥 You had intense Sparring Matches!\n" \
                  f"➕ All Stats +{stat_gain}\n" \
                  f"➕ Gained {xp_gain} XP"
    
    # Check for level up
    level_up = check_level_up(user.id)
    if level_up:
        message += f"\n🌟 Level Up! You are now level {user_data[user.id]['level']}!"
    
    query.edit_message_text(text=message)

# Profile command
def profile(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id not in user_data:
        update.message.reply_text("Please create your ninja profile first with /create!")
        return
    
    clan_icon = {
        "uzumaki": "🍃",
        "uchiha": "⚡",
        "hyuga": "💧",
        "senju": "🔥"
    }.get(user_data[user.id]["clan"], "🌀")
    
    xp_needed = user_data[user.id]["level"] * 100
    xp_progress = min(100, int((user_data[user.id]["xp"] / xp_needed) * 100))
    
    message = f"📜 Shinobi Profile of {user_data[user.id]['name']}\n\n" \
              f"{clan_icon} Clan: {user_data[user.id]['clan'].capitalize()}\n" \
              f"⭐ Level: {user_data[user.id]['level']} | XP: {user_data[user.id]['xp']}/{xp_needed} ({xp_progress}%)\n\n" \
              f"💪 Strength: {user_data[user.id]['stats']['strength']}\n" \
              f"⚡ Speed: {user_data[user.id]['stats']['speed']}\n" \
              f"🌀 Chakra: {user_data[user.id]['stats']['chakra']}\n" \
              f"📘 Intelligence: {user_data[user.id]['stats']['intelligence']}\n\n" \
              f"Use /train to improve your skills or /battle to test your might!"
    
    if "photo" in user_data[user.id] and user_data[user.id]["photo"]:
        update.message.reply_photo(
            photo=user_data[user.id]["photo"],
            caption=message
        )
    else:
        update.message.reply_text(message)

# Help command
def help_command(update: Update, context: CallbackContext) -> None:
    help_text = "🍃 Naruto Legacy Bot Commands 🍃\n\n" \
                "/start - Begin your ninja journey\n" \
                "/create - Create your shinobi profile\n" \
                "/story - Experience the Naruto story\n" \
                "/battle - Fight against enemies\n" \
                "/train - Improve your ninja skills\n" \
                "/profile - View your shinobi profile\n" \
                "/help - Show this help message\n\n" \
                "🔥 Your adventure awaits, Shinobi!"
    
    update.message.reply_text(help_text)

# Error handler
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("create", create))
    dispatcher.add_handler(CommandHandler("story", story))
    dispatcher.add_handler(CommandHandler("battle", battle))
    dispatcher.add_handler(CommandHandler("train", train))
    dispatcher.add_handler(CommandHandler("profile", profile))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("skip", skip_photo))

    # Register callback handlers
    dispatcher.add_handler(CallbackQueryHandler(clan_selection, pattern='^(uzumaki|uchiha|hyuga|senju)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_story_choice, pattern='^chapter_'))
    dispatcher.add_handler(CallbackQueryHandler(handle_battle_action, pattern='^battle_'))
    dispatcher.add_handler(CallbackQueryHandler(handle_training, pattern='^train_'))

    # Register message handlers
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    # Register error handler
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
