using Microsoft.EntityFrameworkCore;
using FrontendMentorAPI.Models;

namespace FrontendMentorAPI.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<Product> Products { get; set; }
    }
}
