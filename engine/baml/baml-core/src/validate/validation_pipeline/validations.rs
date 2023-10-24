mod classes;
mod enums;
mod variants;

use super::context::Context;

pub(super) fn validate(ctx: &mut Context<'_>) {
    enums::validate(ctx);
    classes::validate(ctx);
    variants::validate(ctx);
}
