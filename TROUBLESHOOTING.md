# FastAPI MongoDB Deployment - Troubleshooting

## ❌ Authentication Failed Error

Your MongoDB connection is failing with: `bad auth : authentication failed`

### 🔧 Fix Instructions:

1. **Verify MongoDB Credentials**
   - Go to [MongoDB Atlas](https://cloud.mongodb.com)
   - Login to your account
   - Navigate to your cluster
   - Click "Connect" → "Drivers" → "Python"
   - Copy the correct connection string

2. **Update Connection String**
   - Open `.env` file in your project
   - Replace the `MONGO_URL` with your correct credentials:
   ```
   MONGO_URL=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/
   ```

3. **Common Issues:**
   - ❌ Special characters in password not URL-encoded (use @ as %40, # as %23, etc.)
   - ❌ Wrong username/password combination
   - ❌ IP address not whitelisted in MongoDB Atlas
   - ❌ Database user doesn't have proper permissions

4. **Whitelist Your IP**
   - Go to MongoDB Atlas → Network Access
   - Click "Add IP Address"
   - Add your current IP or use 0.0.0.0/0 for development

5. **Test Connection**
   ```bash
   python test_db.py
   ```

6. **Restart Application**
   ```bash
   python -m uvicorn main:app --reload
   ```

## ✅ API Health Check

After fixing the connection, visit:
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs

Both should return success if the database is properly connected.
