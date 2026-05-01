from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),  # Бұрынғы migration атауы
    ]

    operations = [
        migrations.CreateModel(
            name='DirectMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sent_messages',
                    to='myapp.userprofile'
                )),
                ('receiver', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='received_messages',
                    to='myapp.userprofile'
                )),
            ],
            options={'ordering': ['created_at']},
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user1', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='conversations_as_user1',
                    to='myapp.userprofile'
                )),
                ('user2', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='conversations_as_user2',
                    to='myapp.userprofile'
                )),
                ('last_message', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='+',
                    to='myapp.directmessage'
                )),
            ],
            options={'ordering': ['-updated_at'], 'unique_together': {('user1', 'user2')}},
        ),
    ]