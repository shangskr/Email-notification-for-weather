# 邮箱天气推送

本项目利用GitHub Action实现了通过电子邮件推送天气信息的功能。

## 如何使用

1. 克隆该仓库：
2. 创建一个OpenWeatherMap的API密钥，详细信息请访问 [OpenWeatherMap](https://openweathermap.org/)。
3. 将你的OpenWeatherMap API密钥添加到GitHub Secrets中。在你的GitHub仓库中，转到Settings > Secrets，然后添加一个名为`OPENWEATHERMAP_API_KEY`的新密钥，将你的API密钥作为值。
4. 你需要配置的环境变量（`API_KEY`和`OPENWEATHERMAP_API_KEY`配置一样，`EMAIL_PASSWORD`要使用SMTP服务的应用码而不是邮箱密码）：
   - `API_KEY`
   - `CITY`
   - `EMAIL_PASSWORD`
   - `OPENWEATHERMAP_API_KEY`
   - `RECEIVER_EMAIL`
   - `SENDER_EMAIL`
5. 在GitHub仓库的Settings中的Actions页面，确保开启了`Read and write permissions`和`Allow GitHub Actions to create and approve pull requests`。
6. 其中send_weather_email.py中第50行(`smtp.office365.com', 587`)请自行修改，我用到的是Outlook的SMTP和端口。另外，在`.github/workflows/daily_weather_notification.yml`中，第28行 `CITY: "xingtai"` # 替换成你要查询的城市名，城市名称请前往OpenWeatherMap查看。
