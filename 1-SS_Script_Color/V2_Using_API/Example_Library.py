from supersetapiclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="admin",
)

#dashboards = client.dashboards.find()
#print(dashboards)

dashboard = client.dashboards.find(id=20)[0]
print(dashboard.colors)
#print(dashboard.json_metadata)


dashboard.update_colors({
    "Ingresadasss": "#fcba03"
})

# Save all changes
dashboard.save()