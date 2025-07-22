# Odoo Agriculture Management Module - Troubleshooting Guide

## Çözülen Sorunlar:
✅ 'mail' dependency eklendi - mail.thread ve mail.activity.mixin hatalarını çözer
✅ Modül dosya yapısı kontrol edildi - Tüm gerekli dosyalar mevcut
✅ Syntax hataları kontrol edildi - Python syntax hataları yok

## Modülü çalıştırmak için:

1. **Odoo config dosyasında addons_path kontrolü:**
   ```
   addons_path = /path/to/odoo/addons,/path/to/enterprise/addons,c:\odoo_custom_addons
   ```

2. **Odoo server restart:**
   ```bash
   ./odoo-bin -c /path/to/odoo.conf --dev=all
   ```

3. **Database update:**
   - Apps menüsünden "Agriculture Management" modülünü arayın
   - "Update" butonuna tıklayın
   - Veya command line'dan: `./odoo-bin -c odoo.conf -u agriculture_management_odoo -d your_database`

4. **Log kontrolü:**
   Odoo loglarını kontrol edin:
   ```bash
   tail -f /var/log/odoo/odoo.log
   ```

## Olası diğer hatalar:
- Database migration issues
- Missing external dependencies  
- Version compatibility issues (modül Odoo 17.0 için yazılmış)
- Access rights problems

## Debug için:
1. Developer mode'u açın
2. Technical → Database Structure → Models menüsünden modellerinizi kontrol edin
3. Settings → Users & Companies → Groups'tan yetkileri kontrol edin
