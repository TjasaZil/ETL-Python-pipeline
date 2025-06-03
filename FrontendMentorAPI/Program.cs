using FrontendMentorAPI.Data;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddControllers();
// ... other services (e.g., CORS, see next section) ...

var app = builder.Build();
// ... app configuration ...
app.MapControllers();
app.Run();
