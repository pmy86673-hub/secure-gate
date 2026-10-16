from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
import os

app = FastAPI()

# مخزن الرموز: هنا تتحكم بالمستخدمين والروابط السحرية
DATABASE = {
    "user_secret_token_1": {
        "target_url": "https://google.com",  # 👈 امسح جوجل وضَع رابط قارئ الأكواد الأصلي الخاص بك هنا
        "is_used": False
    },
    "user_secret_token_2": {
        "target_url": "https://google.com",  # 👈 ضع رابطك الأصلي هنا أيضاً للمستخدم الثاني
        "is_used": False
    }
}

@app.get("/open-link/{token}")
def check_and_redirect(token: str):
    # 1. التحقق من وجود الرمز داخل الكائن السري
    if token not in DATABASE:
        raise HTTPException(status_code=404, detail="عذراً، هذا الرابط غير صالح أو غير مسجل لدينا!")
    
    # 2. التحقق مما إذا كان الكائن قد استُخدم سابقاً وأصبح فارغاً
    if DATABASE[token]["is_used"]:
        raise HTTPException(status_code=403, detail="عذراً، تم استخدام هذا الرابط لمرة واحدة سابقاً وانتهت صلاحيته!")
    
    # 3. قفل الكائن فوراً وتحويل حالته إلى "مستعمل" لمنع الدخول مرة ثانية
    DATABASE[token]["is_used"] = True
    
    # 4. توجيه المستخدم تلقائياً للرابط الأصلي في متصفح هاتفه
    return RedirectResponse(url=DATABASE[token]["target_url"])

if __name__ == "__main__":
    # هذا السطر يضمن أن يعمل السيرفر بالمنفذ العالمي المتغير الذي تفرضه منصات الرفع
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
